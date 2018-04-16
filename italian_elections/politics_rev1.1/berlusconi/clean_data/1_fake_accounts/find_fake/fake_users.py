import json
import requests
import time
import bs4 as bs
import contextlib
import urllib
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

parser.add_argument('-d','--database',nargs="?",
                    help='Supply a database name. Here the number of likes, comments,\
                    pic_shortcode,username and comment texts will be stored.''')

#ugly variables
RX_SHARED_DATA = re.compile(r'window._sharedData = ({[^\n]*});')
NO_RESIZE_RX = re.compile(r'(/[p|s][0-9]*x[0-9]*)')
RX_TEMPLATE = re.compile(r'{([a-zA-Z]*)}')
RX_CODE_URL = re.compile(r'p/([^/]*)')

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

    cursor.execute("""CREATE TABLE IF NOT EXISTS fake_users(
                                                           username  varchar(4000),
                                                           comment_text varchar(4000),
                                                           biography varchar(4000),
                                                           following int,
                                                           followers int,
                                                           n_posts int
                                                           );""")
    return conn



def open_database(database):


    try:
        conn = sqlite3.connect(database)
        conn.text_factory  =str
    except sqlite3.Error as e:
        print(e)
        sys.exit(-1)
    return conn

def login(username,password,database,connection):
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
            users = call_users(database)
            #eliminitate duplicates
            new_users = []
            for user in users:
                if user in new_users:
                    continue
                else:
                    new_users.append(user)
            #we can parallelize here
            for user in new_users:
                target = user
                page_name = "ProfilePage"
                section_name = "user"
                base_url = "https://www.instagram.com/{}/"
                #retrieve all the pages with pictures
                retrieve_pages(database,connection,session,target,page_name,section_name,base_url)


def call_users(database):

    cursor = database.cursor()
    command= cursor.execute('''SELECT username FROM politics;''')
    users = []
    for row in command.fetchall():
        #print(row[0])
        users.append(row[0])
    return users

def retrieve_pages(database,connection,session,target,page_name,section_name,base_url):

    #collect all the urls to scrape
    photo_urls = [] #create a list of urls to be processed then
    current_page = 0
    url = base_url.format(target)
    #urls.append(url)
    print("Scraping : %s" % url) #sanity check
    #print("Retrieving urls...")
    #connect to the url and read all the infor
    new_connection = session.get(url,verify=True) #get the url of the user
    data =  get_shared_data(new_connection)
    #check if the profile does exists
    try:
        following=data['entry_data'][page_name][0][section_name]["followed_by"]["count"]
        follower=data['entry_data'][page_name][0][section_name]["follows"]["count"]
        if following==0:
            following=1
        if follower==0:
            follower=1
        print(float(following/follower))
        ratio = float(following/follower)
        if ratio>=5.0:
            #save their comments
            #how many follwoers and following
            #how many posts
            #biography
            #some of them are working on mediaset
            username = data['entry_data'][page_name][0][section_name]["username"]#.encode("utf-8")
            biography = (data['entry_data'][page_name][0][section_name]["biography"])#.encode("utf-8"))
            followers =   int(data['entry_data'][page_name][0][section_name]["followed_by"]["count"])
            following =  int(data['entry_data'][page_name][0][section_name]["follows"]["count"])
            n_posts = int(data["entry_data"][page_name][0]["user"]["media"]["count"])
            print(n_posts)
            print(username,followers,following, n_posts)

            cursor = database.cursor()
            comm_command = cursor.execute('''SELECT comment_text FROM politics WHERE username="%s" '''
                                    % username)


            conn_cursor = connection.cursor()
            for comm in comm_command.fetchall():

                print(username,comm,biography,following,followers,n_posts)
                conn_cursor.execute('''INSERT INTO fake_users(username,comment_text,biography,following,followers,n_posts)
                  VALUES (?,?,?,?,?,?)''',(username,comm[0],biography,following,followers,n_posts) )
                connection.commit()


    except:

        #sleep and re-try
        soup = bs.BeautifulSoup(new_connection.text)
        title = soup.find("title")
        #print(title)
        if "Unavailable" in title.string.split():
            print("User Unavailable")
            #make the system to sleep for a while to retrieve the other data
            time.sleep(5*random.random())
        elif "Not" in title.string.split():
            print("user Unavailable")
            time.sleep(5*random.random())
        else:
            time.sleep(5*random.random())
            retrieve_pages(database,connection,session,target,page_name,section_name,base_url)
    


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


#where to save the database
if args.database:
    database = args.database
else:
    database = os.getcwd()+ "/%s.db" %user

#create the database#
database = open_database(database)
#crate a storing database
connection = create_database("fake_users.db")

login(username,passw,database,connection)
