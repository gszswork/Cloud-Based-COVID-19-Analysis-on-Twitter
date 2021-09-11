"""
@Author: Guangzheng Hu
Student ID: 692277

Description: Fuctions that process data and save processed data into CouchDB
"""
import sys
sys.path.append('../../')
from backend.couchDbHandler import CouchDB

from toolFunc import *
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import pandas as pd
import json
from datetime import timedelta,datetime
from tqdm import tqdm

def make_name_data(name, data):
    resp = {}
    resp['name'] = name
    resp['data'] = data
    return resp

def get_all_hashtags(data):
    hashtags = {}
    for word, frequency in data.items():
        if word.startswith("#") and len(word) > 1:
            hashtags[word] = frequency
    return dict(sorted(hashtags.items(), key=lambda item: item[1],reverse=True))

def get_time_self(elm):
    date = datetime.strptime(elm, '%a %b %d %H:%M:%S +0000 %Y')
    return date

def get_topN(table):
    
    tt = TweetTokenizer()
    delta = timedelta(hours=1)
    
    timeline = {}

    for tweet in tqdm(table):
        text = tweet.key[1]
        if not text:
            text = ''
        time_str = tweet.key[0]#.replace(' ','-')
        time = get_time_self(time_str)
        timeb = datetime(2020,10,1,0,0,0,0)
        while timeb < datetime.now():
            timeS = timeb
            timeE = timeb + delta
            if time > timeS and time < timeE:
                if timeS.strftime('%Y/%m/%d/%H') in timeline:
                    word_freq = timeline[timeS.strftime('%Y/%m/%d/%H')].copy()
                    ll = [w.lower() for w in tt.tokenize(text)]
                    word_freq = get_word_freq(word_freq,ll)
                    timeline[timeS.strftime('%Y/%m/%d/%H')] = word_freq.copy()

                else:
                    word_freq ={}
                    ll = [w.lower() for w in tt.tokenize(text)]
                    word_freq = get_word_freq(word_freq,ll)
                    timeline[timeS.strftime('%Y/%m/%d/%H')] = word_freq.copy()
            timeb += delta

    return timeline

def save_au_heat():
    cdb = CouchDB()
    au_db = cdb.get_db('has_location_try')
    table = au_db.iterview('_design/dictionary/_view/geo',3000,descending=True)
    resp = {}
    resp = precess_au_heatmap(table)
    with open('au_heatmap_mid.json','w') as jj:
        json.dump(resp, jj)
    ic_db = cdb.create_db('au_heatmap')
    #ic_db = cdb.get_db('au_heatmap')
    ic_db['au_heat_new'] = resp
    return resp

def save_hotword():
    cdb = CouchDB()
    e_db = cdb.get_db('melbourne20_21')
    h_db = cdb.get_db('abc')
    table = e_db.iterview('_design/dictionary/_view/textdate',10000)
    #timeline = get_topN(table)
    with open('./data/timeline_all_reduce.json','r') as jj:
        #json.dump(timeline, jj)
        timeline = json.load(jj)

    word_set = set()
    for k,v in timeline.items():
        for word in v.keys():
            word_set.add(word)

    
    for k,v in timeline.items():
        word_list = []
        count_list = []
        for word in list(word_set):
            word_list.append(word)
            if word in v:
                count_list.append(v[word])
            else:
                count_list.append(0)
        print(k, len(word_list),sum(count_list))
        d = {'word': word_list, 'count':count_list}
        h_db[k] = d.copy()
        d = {}

    return timeline

def save_lang_heat():
    cdb = CouchDB()
    au_db = cdb.get_db('melbourne2016')
    rtable = au_db.view('_design/dictionary/_view/reducelanguage',group = True)
    big_resp = {}
    for lang in rtable:
        table = au_db.view('_design/dictionary/_view/language', key = lang.key)
        resp = process_lang_heatmap(table)
        big_resp[lang.key] = resp
    s_db = cdb.create_db('heatmap_lang')
    #s_db = cdb.get_db('heatmap_lang')
    for k,v in big_resp.items():
        print(k)
        s_db[k] = v
    return big_resp

def get_value_list(table):
    big ={}
    for v in table:
        #print(v)
        key = v.key.copy()
        value = v.value
        lang = key[-1]
        if lang not in big:
            print('s')
            big[lang] = []
        if value and ('australia' in value.lower() or 'vic' in value.lower()):
            big[lang].append({'key': key.copy(), 'value': value})
            #print(len(big[lang]))
            #print(big[lang][-1])
        key = []
        value = ''
    print('finish')
    return big


def save_lang_heat_all():
    cdb = CouchDB()
    au_db = cdb.get_db('melbourne2016')
    rtable = au_db.view('_design/dictionary/_view/reducelanguage',group = True)
    f = open('./data/has_loc.json', 'r')
    table_all = json.load(f)
    f.close()
    big_resp = {}
    for lang in rtable:
        table_16 = au_db.view('_design/dictionary/_view/language', key = lang.key)
        print(lang.key)
        if lang.key in table_all:
            resp = precess_au_heatmap(table_all[lang.key], table_16)
            big_resp[lang.key] = resp
    s_db = cdb.create_db('heatmap_lang_all')
    #s_db = cdb.get_db('heatmap_lang_all')
    for k,v in big_resp.items():
        print(k)
        s_db[k] = v
    return big_resp

def save_circle_tweet():
    cdb = CouchDB()
    result_db = cdb.create_db('vic_circle_tweet')
    #result_db = cdb.get_db('vic_circle_tweet')
    f = open('./data/save.json', 'r')
    data = json.load(f)
    for k,v in tqdm(data.items()):
        lga = v[0]
        geo = v[1]
        time = v[2]
        text= v[3]
        lang = v[4]
        d = {'lga': lga, 'geo': geo, 'time': time, 'text':text, 'lang':lang}
        result_db.save(d)

def save_lga_tweet():
    cdb = CouchDB()
    s_db = cdb.get_db('sentiment_location_lga')
    table = s_db.view('_design/dictionary/_view/sentiment')

    resp = process_lga_tweet(table)
    result_db = cdb.create_db('lga_tweet_info')
    #result_db = cdb.get_db('lga_tweet_info')
    result_db['lga'] = resp


save_hotword()
save_lang_heat()
save_lang_heat_all()
save_circle_tweet()
save_lga_tweet()