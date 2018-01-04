import json
import requests
import time
import bs4 as bs
import contextlib
import urllib
import os,sys,datetime, random,re, argparse
#the script is modelled from the wonderful program of Althonos:
#https://github.com/althonos/InstaLooter



parser = argparse.ArgumentParser(description="""lovInstagram: scrape an Instagram account.\n
                                                This script can be used to perform data analyses.\n
                                                Further implementations will be made for a correct analysis of metadata.\n
                                                To scrape a user:\n
                                                python scraper_private.py -u/--user  USERNAME\n""",
                                 epilog="script designed by Stefano Bosisio"
                                        "to gather information from instagram pics ",
                                 prog="lovInsta")

parser.add_argument('-l','--login',nargs="+",
                    type=str,help='Supply username and password for login')

parser.add_argument('-u', '--user', nargs="?",
                    help='Supply a username to scrape a user.')

parser.add_argument('-d','--directory',nargs="?",
                    help='Supply a directory to save all the pics.')

#ugly variables
RX_SHARED_DATA = re.compile(r'window._sharedData = ({[^\n]*});')
NO_RESIZE_RX = re.compile(r'(/[p|s][0-9]*x[0-9]*)')
RX_TEMPLATE = re.compile(r'{([a-zA-Z]*)}')
RX_CODE_URL = re.compile(r'p/([^/]*)')

def login(username,password,directory,user):
    print("Login...")
    URL_HOME = "https://www.instagram.com/"
    URL_LOGIN = "https://www.instagram.com/accounts/login/ajax/"
    #URL_LOGOUT = "https://www.instagram.com/accounts/logout/"
    #extract from  InstaLooter
    session = requests.Session()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
    session.cookies.update({
        'sessionid': '',
        'mid': '',
        'ig_pr': '1',
        'ig_vw': '1920',
        'csrftoken': '',
        's_network': '',
        'ds_user_id': ''
    })
    #here you need to put the user and password
    login_post = {'username': username,
                  'password': password}


    session.headers.update({
        'Origin': URL_HOME,
        'Referer':URL_HOME,
        'X-Instragram-AJAX': '1',
        'X-Requested-With': 'XMLHttpRequest',
    })
    res = session.get(URL_HOME)
    #here I copy the csrftoken, thus it is possible to connect
    session.headers.update({'X-CSRFToken': res.cookies['csrftoken']})
    #we need to make it sleep
    time.sleep(5 * random.random())
    #now login
    login = session.post(URL_LOGIN, data=login_post, allow_redirects=True)
    #now take the csrf token otherwise we cannot access
    session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
    csrftoken = login.cookies['csrftoken']

    if login.status_code != 200:
        csrftoken = None
        raise SystemError("Login error: check your connection")
    else:
        r = session.get(URL_HOME)
        #print(r.text)
        if r.text.find("%s" % username) == -1:
            raise ValueError('Login error: check your login data')
        else:
            print("Login succeed")
            ##SCrape only users
            if user is not None:
                print("Scraping profile %s..." % user)
                target = user
                page_name = "ProfilePage"
                section_name = "user"
                base_url = "https://www.instagram.com/{}/"
                #retrieve all the pages with pictures
                retrieve_pages(directory,session,target,page_name,section_name,base_url)
            else:
                print("Please select an option: profile or hastag")


def retrieve_pages(directory,session,target,page_name,section_name,base_url):

    if not os.path.exists(directory):
        os.makedirs(directory)
    #collect all the urls to scrape
    photo_urls = [] #create a list of urls to be processed then
    current_page = 0
    url = base_url.format(target)
    #urls.append(url)
    print("Scraping : %s" % url) #sanity check
    while True:
        current_page +=1
        #print("Retrieving urls...")
        #connect to the url and read all the infor
        res = session.get(url) #get the url of the user
        data =  get_shared_data(res)
        try:
            media = data['entry_data'][page_name][0][section_name]['media']
            media_info = data['entry_data'][page_name][0][section_name]['media']["nodes"]
            count_photos = 0
            for nodes in media_info:
                photo_url = NO_RESIZE_RX.sub('', nodes.get('display_src'))
                #print(nodes["caption"])
                #caption --> "caption"
                #comments --> "comments"
                #likes --> "likes"
                #print(nodes["code"])
                print("Page %d  photo %d" % (current_page, count_photos))

                #[u'code', u'gating_info', u'dimensions', u'caption',
                #u'thumbnail_resources', u'comments_disabled', u'__typename',
                #u'comments', u'date', u'media_preview', u'likes', u'owner', u'thumbnail_src',
                #u'is_video', u'id', u'display_src']

                #print(media_info["page_info"]["end_cursor"])
                #url = '{}?max_id={}'.format(base_url.format(target), media_info['page_info']["end_cursor"])
                #print(photo_url)
                photo_urls.append(photo_url)
                #filename = make_filename(nodes)
                #print(filename)
                savedfile = directory + "/" + nodes["code"] + ".jpg"#+ filename
                with contextlib.closing(session.get(photo_url)) as image:
                    with open(savedfile,"wb") as dest_file:
                        for block in image.iter_content(1024):
                            if block:
                                dest_file.write(block)
                #open the image with pyexiv2#
                dest_file.close()
                count_photos+=1
        except:
            break

        if not media['page_info']['has_next_page']:
            break

        else:
            url = '{}?max_id={}'.format(base_url.format(target), media['page_info']["end_cursor"])



def get_shared_data(res):
    #here we retrieve the data shared by the user
    PARSER = "html.parser"
    soup = bs.BeautifulSoup(res.text, PARSER)
    #in the soup we have everything we need to take the pictures
    script = soup.find('body').find('script', {'type': 'text/javascript'})
    #here extract the info from the contact
    #you got initially a dictionary from json loads and then extract the values
    media_group = (json.loads(RX_SHARED_DATA.match(script.text).group(1)))

    #Here we could retrieve some info about the user if it's private

    #return private,followed,json.loads(RX_SHARED_DATA.match(script.text).group(1))
    return media_group


#MAIN
args = parser.parse_args()

if args.login:
    #usually we will have 2 input here
    username = args.login[0]
    passw = args.login[1]

if args.user:
    print("Username to scrape %s" % args.user)
    user = args.user
else:
    user = None



if args.directory:
    directory = args.directory
else:
    directory = os.getcwd()




login(username,passw,directory,user)
