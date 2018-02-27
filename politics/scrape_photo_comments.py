import json
import requests
import time
import bs4 as bs
import os,sys,datetime, random,re, argparse
import sqlite3
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

parser.add_argument('-d','--database',nargs="?",
                    help='Supply a database name. Here the number of likes, comments,\
                    pic_shortcode,username and comment texts will be stored.')

#ugly variables
RX_SHARED_DATA = re.compile(r'window._sharedData = ({[^\n]*});')

def create_database(database):
    #Database is the database name, here we will create a
    #connection to X.db

    try:
        conn = sqlite3.connect(database)
        conn.text_factory  =str
    except sqlite3.Error as e:
        print(e)
        sys.exit(-1)
    #the structure of the database is:
    #n_likes, n_comments, shortcode, username_comment, comment_text
    #the icture shortcode it's useful to understand if there have been any
    #point where the candidate has faced serious bad or very good comments
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS politics( n_likes  int,
                                                           n_comments int,
                                                           shortcode varchar(4000),
                                                           username  varchar(4000),
                                                           comment_text varchar(4000)
                                                           );""")
    return conn


def login(username,password,database,user):
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
                retrieve_pages(database,session,target,page_name,section_name,base_url)
            else:
                print("Please select an option: profile or hastag")


def retrieve_pages(database,session,target,page_name,section_name,base_url):

    #collect all the urls to scrape
    current_page = 0
    url = base_url.format(target)
    shortcodes = []#create a list for storing shortcodes
    print("Scraping : %s" % url) #sanity check
    while True:
        current_page +=1
        #print("Retrieving urls...")
        #connect to the url and read all the infor
        res = session.get(url,verify=True) #get the url of the user
        data =  get_shared_data(res)
        try:
            media = data['entry_data'][page_name][0][section_name]['media']
            media_info = data['entry_data'][page_name][0][section_name]['media']["nodes"]
            count_photos = 0
            for nodes in media_info:
                #print(nodes["code"])
                shortcodes.append(nodes["code"])
        except:
            break

        if not media['page_info']['has_next_page']:
            break

        else:
            url = '{}?max_id={}'.format(base_url.format(target), media['page_info']["end_cursor"])


    print("Comments scraping...")
    for code in shortcodes:
        url = "https://www.instagram.com/p/%s/" % code
        res  = session.get(url,verify=True)
        data = get_shared_data(res)
        comments = (data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_media_to_comment"]["edges"])
        c_comments =data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_media_to_comment"]["count"]
        n_likes = (data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_media_preview_like"]["count"])
        timestamp = (data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["taken_at_timestamp"])
        #check if the  post was done during the election campaign
        real_day = datetime.datetime.fromtimestamp(timestamp)
        if (real_day.month >=1 and real_day.year>=2018):
            #n_likes, n_comments, shortcode, username_comment, comment_text
            for comment in comments:
                comm_username = comment["node"]["owner"]["username"].encode("utf-8")
                comm_text     = comment["node"]["text"].encode("utf-8")
                #add everything to the database
                cursor=database.cursor()
                cursor.execute('''INSERT INTO politics(n_likes,n_comments,shortcode,username,comment_text)
                                  VALUES (?,?,?,?,?)''',(n_likes,c_comments,code,comm_username,comm_text) )
                database.commit()

        else:
            continue


    print("Finish scraping :)")


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

#login
if args.login:
    #usually we will have 2 input here
    username = args.login[0]
    passw = args.login[1]
#who do you want to scrape?
if args.user:
    print("Username to scrape %s" % args.user)
    user = args.user
else:
    user = None

#where to save the database
if args.database:
    database = args.database
else:
    database = os.getcwd()+ "/%s.db" %user

#create the database#
connection = create_database(database)

login(username,passw,connection,user)
