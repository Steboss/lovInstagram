import copy, os, sys, datetime, re,copy
import json, random, warnings, requests
import six, time
import bs4 as bs
import contextlib
import argparse
import multiprocessing
from functools import partial
from PIL import Image
import sqlite3
from sqlite3 import Error

#TODO add geoplot to  draw maps
#TODO add username and passw for login
#TODO add metadata to photos
#TODO fix tags

parser = argparse.ArgumentParser(description="""lovInstagram: scrape an Instagram account or hashtag.\n
                                                This script can be used to perform data analyses.\n
                                                Further implementations will be made for a correct analysis of metadata.\n
                                                To scrape a user:\n
                                                python scraper_private.py -u/--user  USERNAME\n
                                                To scraper a hashtag or more hashtag:\n
                                                python scraper_private.py -a/--hashtag hashtag1 hashtag2 hashtag3\n""",
                                 epilog="script designed by Stefano Bosisio"
                                        "to gather information from instagram pics ",
                                 prog="lovInsta")

parser.add_argument('-a','--hashtag',nargs="+", #+ so we can give multiple inputs of strings
                    type=str,help='Supply a hashtag to scrap hashtag pics.')

parser.add_argument('-d','--directory',nargs="?",
                    help='Supply a directory to save all the pics.')

RX_SHARED_DATA = re.compile(r'window._sharedData = ({[^\n]*});')
NO_RESIZE_RX = re.compile(r'(/[p|s][0-9]*x[0-9]*)')
RX_TEMPLATE = re.compile(r'{([a-zA-Z]*)}')
RX_CODE_URL = re.compile(r'p/([^/]*)')
#maybe bring URL_HOME/LOGIN/LOGOUT and Profile and Hashtag as global variables



def login(directory,hashtag):

    for tag in hashtag:
        print("Scraping tag %s..." %tag)
        target= tag
        page_name = "TagPage"
        section_name = "tag"
        base_url="https://www.instagram.com/explore/tags/{}"
        pages(directory,target,page_name,section_name,base_url)


def pages(directory,target,page_name,section_name,base_url):


    if not os.path.exists(directory):
        os.makedirs(directory)


    url = base_url.format(target)
    print("Scraping : %s" % url) #sanity check
    #now get the data
    res = requests.get(url,verify=True)
    soup = bs.BeautifulSoup(res.text, "html.parser")
    script = soup.find('body').find('script', {'type': 'text/javascript'})
    json_string = json.loads(RX_SHARED_DATA.match(script.text).group(1))
    #collect the ids
    query_ids = get_query_id(res)
    #now cycle through these first  values
    nodes = (json_string["entry_data"]["TagPage"][0]["graphql"]["hashtag"]["edge_hashtag_to_media"])
    for node in nodes["edges"]:
        text = node["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
        timestamp = node["node"]["taken_at_timestamp"]
        real_day = datetime.datetime.fromtimestamp(timestamp)
        owner_id = int(node["node"]["owner"]["id"])
        #owner_username, full_name, biography, followers, following = get_username_alternative(owner_id)
        likes = int(node["node"]["edge_liked_by"]["count"])
        n_comms = int(node["node"]["edge_media_to_comment"]["count"])
        #print(owner_username,full_name,followers,following)
        #check between 1st/1/2018 and today
        if (real_day.month>=1 and real_day.year==2018):
            print()
            #print(owner_id,text,likes,n_comms)
        else:
            continue


    #now go on with the other hashtag
    while True:
        try:
            has_next_page = nodes["page_info"]["has_next_page"]
            if has_next_page:
                end_cursor = nodes["page_info"]["end_cursor"]
                url= "https://www.instagram.com/graphql/query/?query_hash=%s&tag_name=%s&first=12&after=%s" % (
                    query_ids[0], target, end_cursor) #try the first query_id
                #connect
                res = requests.get(url,verify=True).json() # this is already a json
                #print(res.keys())
                nodes = (res["data"]["hashtag"]["edge_hashtag_to_media"])
                for node in nodes["edges"]:

                    text = node["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
                    timestamp = node["node"]["taken_at_timestamp"]
                    real_day = datetime.datetime.fromtimestamp(timestamp)
                    owner_username, full_name, biography, followers, following = get_username_alternative(owner_id)
                    likes = int(node["node"]["edge_liked_by"]["count"])
                    n_comms = int(node["node"]["edge_media_to_comment"]["count"])
                    print(owner_username,full_name,followers,following)
                    #check between 1st/1/2018 and today
                    if (real_day.month>=1 and real_day.year==2018):
                        test = real_day
                        #print(owner_id,text,likes,n_comms)
                    else:
                        continue

        except:
            break
    #print(len(posts))



def get_query_id(res):
    #from the  initial url we need to find the javascript ConsumerCommons:
    queryids = []
    soup = bs.BeautifulSoup(res.text)
    for script in soup.find_all("script"):
        if script.has_attr("src"):# and "ConsumerCommons" in script["src"]:
            text = requests.get("https://www.instagram.com%s" % script["src"]).text
            #print("https://www.instagram.com%s" % script["src"])
            for query_id in re.findall(r"queryId:\"(.+?)\",",text):
                queryids.append(query_id)
                print(query_id)

    return queryids




def get_shared_data(res,base_url,target):

    PARSER = "html.parser"


    return json_string

def get_username_alternative(owner_id):

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"})
    base_url= """https://www.instagram.com/graphql/query/?query_id=17888483320059182&variables={"id":"%d","first":1,"after":""}""" % owner_id
    #use a new session
    response = session.get(base_url)
    #here I copy the csrftoken, thus it is possible to connect
    session.headers.update({'X-CSRFToken': response.cookies['csrftoken']})
    time.sleep(5 * random.random())
    json_string = response.json()
    if json_string["status"]=="fail":
        #make it sleep 5 min and skip this user
        time.sleep(300)
        #recall the function
        get_username_alternative(owner_id)
    else:
        #print(json_string)
        shortcode=(json_string["data"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["shortcode"])
        base_url="""https://www.instagram.com/p/%s/?__a=1""" % shortcode
        response = requests.get(base_url)
        json_string=response.json()["graphql"]["shortcode_media"]
        username=(json_string["owner"]["username"])
        full_name = json_string["owner"]["full_name"]
        #retrieve the other info
        base_url="""https://www.instagram.com/%s/""" % username
        response = requests.get(base_url)
        PARSER = "html.parser"
        soup = bs.BeautifulSoup(response.text, PARSER)
        script = soup.find('body').find('script', {'type': 'text/javascript'})
        json_string = json.loads(RX_SHARED_DATA.match(script.text).group(1))
        user = json_string["entry_data"]["ProfilePage"][0]["user"]
        biography = user["biography"]
        followers = user["followed_by"]["count"]
        following = user["follows"]["count"]
        return username, full_name, biography, followers, following

#MAIN
args = parser.parse_args()


if args.hashtag:
    hashtag = []
    for tag in args.hashtag:
        print("Hashtag to scrape %s" % tag)
        hashtag.append(tag)
else:
    hashtag=None

if args.directory:
    directory = args.directory
else:
    directory = os.getcwd()

login(directory,hashtag)
