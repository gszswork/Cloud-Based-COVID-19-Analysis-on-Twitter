import requests
import json
from datetime import datetime
import argparse
import time
import couchdb
from couchdb.client import Server

secure_remote_server = Server('http://admin:admin@172.26.133.210:5984/')

#db = secure_remote_server.create('melbourne2020')




parser = argparse.ArgumentParser(description='COMP90024 Project Scrape Research Data')
parser.add_argument('--batch', type=int, default=100)
parser.add_argument('--total_forMonth', type=int, default=200000)
parser.add_argument('--location', type=str, default= 'melbourne')
parser.add_argument('--start', type=str, default='2018,1,1')
parser.add_argument('--year', type=int, default=2018)
parser.add_argument('--monthlength', type=int, default=12)
parser.add_argument('--end', type=str, default='2018,12,31')

args = parser.parse_args()
# argsparser
url = 'http://couchdb.socmedia.bigtwitter.cloud.edu.au/twitter/_design/twitter/_view/summary'
BATCHSIZE = args.batch
#该地区在sydney那里

start_key = '[\"'+ args.location +'\",'+args.start +']'
end_key = '[\"'+ args.location +'\",'+args.end +']'
month = args.monthlength
serverName = args.location+str(args.year)
try:
    db = secure_remote_server.create(serverName)
except:
    print('database already exist!!')
params={'include_docs':'true','reduce':'false','start_key':start_key,'end_key':end_key,"skip": "0", "limit": str(BATCHSIZE)}
TOTALSIZE = args.total_forMonth

count = 1
tweetlist = []
while count<=month:
    num = 0
    time = None
    message=requests.get(url,params,auth=('readonly', 'cainaimeeshaLu4Lejoo9ooW4jiopeid'))
    dataset = message.json()
    if len(dataset["rows"]) == 0:
              
            date = args.start[0:5] + str(count) + args.start[-2:]
            print('no',count)
            count += 1 
            params['start_key'] = '[\"'+ args.location +'\",'+ date +']'
            continue 
    while num<TOTALSIZE:
        message=requests.get(url,params,auth=('readonly', 'cainaimeeshaLu4Lejoo9ooW4jiopeid'))
        

        num = num + BATCHSIZE

        temp = num
        params['skip'] = str(temp)

        # Message to dict
        dataset = message.json()
 
    # retrive all tweets
        tweetlst = dataset["rows"]
        
        print(str(num) + "Tweets scraped")
        for tweet in tweetlst:
            try:
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
                if len(dataDict['geo']) > 0: 
                    doc_id, doc_rev = db.save(dataDict)

            except Exception as e:

                print(e)
                print("Cannot upload a well-formatted tweet to couchDB")
    count += 1
    
    date = args.start[0:5] + str(count) + args.start[-2:]
    params['start_key'] = '[\"'+ args.location +'\",'+ date +']'