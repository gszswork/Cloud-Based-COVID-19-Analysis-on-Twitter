from loaddb import *
import re
from textblob import TextBlob
from tqdm import tqdm
from datetime import datetime
#base on the time, we calculate the sentiment score
def get_time(elm):
    date = datetime.strptime(elm, '%a-%b-%d-%H:%M:%S-+0000-%Y')
    return date

def clean_dataset(text):
    # Remove hashtag while keeping hashtag text
    text = re.sub(r'#','', text)
    # Remove HTML special entities (e.g. &amp;)
    text = re.sub(r'\&\w*;', '', text)
    # Remove tickers
    #text = re.sub(r'\$\w*', '', text)
    # Remove hyperlinks
    #text = re.sub(r'https?:\/\/.*\/\w*', '', text)
    # Remove whitespace (including new line characters)
    text = re.sub(r'\s\s+','', text)
    text = re.sub(r'[ ]{2, }',' ',text)
    # Remove URL, RT, mention(@)
    text=  re.sub(r'http(\S)+', '',text)
    text=  re.sub(r'http ...', '',text)
    text=  re.sub(r'(RT|rt)[ ]*@[ ]*[\S]+','',text)
    text=  re.sub(r'RT[ ]?@','',text)
    text = re.sub(r'@[\S]+','',text)
    
    return text


def get_sentiment(table):
    
    delta = timedelta(hours=1)
    
    timeline = {}

    for tweet in tqdm(table):
        text = tweet.key[1]
        
        time_str = tweet.key[0].replace(' ','-')
        time = get_time(time_str)
        timeb = datetime(2020,1,1,0,0,0,0)
        while timeb < datetime.now():
            timeS = timeb
            timeE = timeb + delta
            if time > timeS and time < timeE:
                if timeS.strftime('%Y/%m/%d/%H') in timeline:
                    text = clean_dataset(text)
                    testimonial = TextBlob(text)
                    timeline[timeS.strftime('%Y/%m/%d/%H')].append(testimonial.sentiment.polarity)
                    
                else:
                    text = clean_dataset(text)
                    testimonial = TextBlob(text)
                    timeline[timeS.strftime('%Y/%m/%d/%H')] = [testimonial.sentiment.polarity]
            timeb += delta
        #print(timeline.keys())

    return timeline

import json
from datetime import timedelta
cdb = CouchDB()
e_db = cdb.get_db('melbourne20_21')

table = e_db.iterview('_design/dictionary/_view/textdate',3000)
timeline = get_sentiment(table)

sentiment = {}
for k,v in timeline.items():
    count = 0
    score = []
    for i in v:
        if i != 0:
            score.append(i)
    sentiment[k] = {'sentiment_score':round(sum(score)/(len(score)),4)}


a = cdb.create_db('sentiment_analysis_pre')
h_db = cdb.get_db('sentiment_analysis_pre')


for k,v in sentiment.items():
    h_db[k] = v