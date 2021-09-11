import requests
import json
from datetime import datetime
import argparse
import time
import couchdb
from couchdb.client import Server

from datetime import datetime, timedelta

def get_time(elm):
    if '[' not in elm:
        date = datetime.strptime(elm, '%a-%b-%d-%H:%M:%S-+0000-%Y')
    else:
        date = datetime.strptime(elm, '[\"melbourne\",%Y,%m,%d]')
    return date

def next_date(date):
    delta = timedelta(days=1)
    date += delta
    if date.strftime('%d')[0] != '0' and date.strftime('%m')[0] != '0':        
        date_str = '[\"'+ 'melbourne' +'\",'+ date.strftime('%Y,%m,%d') +']'
    elif date.strftime('%d')[0] == '0' and date.strftime('%m')[0] != '0':   
        date_str = '[\"'+ 'melbourne' +'\",'+ date.strftime('%Y,%m,')+date.strftime('%d')[-1] +']'
    elif date.strftime('%d')[0] != '0' and date.strftime('%m')[0] == '0': 
        date_str = '[\"'+ 'melbourne' +'\",'+ date.strftime('%Y,')+date.strftime('%m')[-1]+date.strftime(',%d') +']'
    else:        
        date_str = '[\"'+ 'melbourne' +'\",'+ date.strftime('%Y,')+date.strftime('%m,')[-2:] +date.strftime('%d')[-1]+']'
    return date_str



secure_remote_server = Server('http://admin:admin@172.26.133.210:5984/')

#db = secure_remote_server.create('melbourne2020')

parser = argparse.ArgumentParser(description='COMP90024 Project Scrape Research Data')
parser.add_argument('--batch', type=int, default=1000)
parser.add_argument('--total_forday', type=int, default=2000)
parser.add_argument('--startkey', type=str, default='[\"melbourne\",2020,12,10]')
parser.add_argument('--endkey', type=str, default='[\"melbourne\",2020,12,10]')
parser.add_argument('--dbname', type=str, default='twitter_raw')
args = parser.parse_args()
# argsparser
url = 'http://couchdb.socmedia.bigtwitter.cloud.edu.au/twitter/_design/twitter/_view/summary'
BATCHSIZE = args.batch
tweet_perday = 10000
#该地区在sydney那里


start_key = args.startkey
end_key = args.endkey
end_year = get_time(end_key).year
end_month = get_time(end_key).month
end_day = get_time(end_key).day
date_str = start_key
serverName = args.dbname

try:
    db = secure_remote_server.create(serverName)
    
except:
    print('database already exist!!')
    db = secure_remote_server[serverName]
params={'include_docs':'true','reduce':'false','start_key':start_key,'end_key':end_key,"skip": "0", "limit": str(BATCHSIZE)}
TOTALSIZE = args.total_forday

count = 1


while True:
    params['start_key'] = date_str
    params['end_key'] = date_str
    print(params['start_key'],params['end_key'])

    date = get_time(date_str)
    if date > datetime(end_year,end_month,end_day):
        break
    num = 0
    params['skip'] = str(0)
    while num<TOTALSIZE:
        try:
            
            message=requests.get(url,params,auth=('readonly', 'cainaimeeshaLu4Lejoo9ooW4jiopeid'))
            num = num + BATCHSIZE
            temp = num
            params['skip'] = str(temp)
            
            dataset = message.json()
            tweetlst = dataset["rows"]
            print(str(num) + "Tweets scraped")
            count = 0
            for tweet in tweetlst:
                try:
                    if count%7 == 0:
                        dataDict = {}
                        dataDict["id"] = tweet["id"]
                        dataDict["user"] = tweet["doc"]["user"]["screen_name"]
                        dataDict["user_id"] = tweet["doc"]["user"]['id']
                        dataDict["text"] = tweet["doc"]["text"]
                        
                        if tweet["doc"]["created_at"] != None:
                            stringTime = tweet["doc"]["created_at"]
                            dataDict["date"] = datetime.strptime(stringTime,'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S%z')
                            dataDict['Create_data'] = stringTime
                        else:
                            dataDict["date"] = ""
                        dataDict["hashtags"] = []
                        if tweet["doc"]["entities"]["hashtags"] != None:
                            listHashtags = tweet["doc"]["entities"]["hashtags"]
                            for hashtag in listHashtags:
                                if "text" in hashtag.keys():
                                    dataDict["hashtags"].append(hashtag["text"])



                        if tweet["doc"]["coordinates"]!= None and tweet["doc"]["coordinates"]["coordinates"] != None:
                            dataDict["geo"] = tweet["doc"]["coordinates"]["coordinates"]	

                        elif tweet["doc"]["geo"]!= None and tweet["doc"]["geo"]["coordinates"] != None:

                            temp = tweet["doc"]["geo"]["coordinates"]
                            if len(temp) == 2:
                                dataDict["geo"] = [temp[1], temp[0]]

                        else:
                            dataDict["geo"] = []
                        
                        dataDict['retweet'] = tweet["doc"]['retweet_count']
                        dataDict['favorite'] = tweet['doc']['favorite_count']
                        dataDict['language'] = tweet['doc']['lang']
                        a = dataDict['text'].split(' ')
                        if (len(a)>5):
                            doc_id, doc_rev = db.save(dataDict)
                    count += 1
                except Exception as e:
                    print(e)
                    print("Cannot upload a well-formatted tweet to couchDB")
        except:
            print(date_str,message)
            continue
    date_str = next_date(date)



