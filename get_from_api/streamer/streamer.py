# this code is used to listen to the tweets in real time.

# Author: yalan zhao
# Student id: 1047739
# Team: COMP90024 - team 24
import time
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
import json
import re

# get the auth

consumer_key = 'GRlbdng3hBwXQIruYflYdOwla'
consumer_secret = '1svXluj7mqB2d0WdCZFdnEDpwKRQV7Ow86VGWBskBfZQKElsRO'

access_token = '1390628851705802754-xRPS5Coqw6UkJ7T4vojBKYfXhb5crX'
access_token_secret = 'iyxHQTaBTK4KoV4TCzFb4JYd8vHUPL90MzkGZtaxn3yKp'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#set the keyword and save to th database
def processdata(data):
    dict={}
    dict['id']=data['id_str']
    dict['key']='Australia'
    dict['doc']=data
    db.save(dict)

#define the listener
class LocateListener(StreamListener):

    def __init__(self):
        super().__init__()

    def on_data(self, data):
        tweetJson = json.loads(data, encoding= 'utf-8')
        print('1')
        # uif the tweet has geo information
        if tweetJson['geo']!=None or tweetJson['coordinates'] or tweetJson['place']:   
            #limit the speed  
            
            time.sleep(1)
            processdata(tweetJson)
        return True

    def on_error(self, status):
        print (status)

# connect the database
import couchdb
server = couchdb.Server('http://admin:admin@172.26.134.73:5984/')
try:
    db = server.create('twitter_streamer')

except:
    print('database already exist!')
    db = server['twitter_streamer']


listener = LocateListener()
stream = tweepy.Stream(auth,listener)
stream.filter(locations = [111,-44,155,-9])

