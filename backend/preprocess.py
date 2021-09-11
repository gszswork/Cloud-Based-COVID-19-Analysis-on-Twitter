"""
@Author: Guangzheng Hu
Student ID: 692277

Description: This file is an experienment file that process datas and save them into CoudhDB
"""
from couchDbHandler import *
from api.toolFunc import *
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

def get_cases():
    case = pd.read_csv('./api/data/case.csv')
    cdb = CouchDB()
    db = cdb.get_db('australia_location')
    loc = db.get('f03a9af2e5923e35a8bbb528b1590ac4')
    resp = precess_case(case, loc, list(loc.keys()))
    return resp

def get_lang():
    dataset = pd.read_csv('./api/data/language_spoken_at_home.csv')
    f = open('./api/data/vic_geo.json','r')
    vic_loc = json.load(f)
    f.close()
    vic_real_name = []
    for i in vic_loc['features']:
        vic_real_name.append(i['properties']['vic_lga__3'])
    f.close()
    resp = precess_lang(dataset, vic_real_name)

    return resp


def save_area_rent_income_crime():
    crime = pd.read_csv('./api/data/crime.csv').fillna(0)
    income = pd.read_csv('./api/data/income.csv').fillna(0)
    rent = pd.read_csv('./api/data/rent.csv').fillna(0)

    f = open('./api/data/vic_geo.json','r')
    vic = json.load(f)
    f.close()
    loc = []
    for i in vic['features']:
        loc.append(i['properties']['vic_lga__3'])
    resp = {}
    for i in range(len(rent)):
        area = rent.loc[i, ' lga_name16']
        value = rent.loc[i, ' median_sep_2017']
        area_name = wash_lga_name(area,loc)
        if area_name in loc:
            if area_name in resp:
                resp[area_name]['rent'] = int(value)
            else:
                resp[area_name] = {}
                if 'a' not in str(value):
                    resp[area_name]['rent'] = int(value)
                else:
                    resp[area_name]['rent'] = value

    for i in range(len(income)):
        area = income.loc[i, ' lga_name16']
        mean = income.loc[i, ' mean_aud_2014_15']
        median = income.loc[i, 'median_aud_2014_15']
        area_name = wash_lga_name(area, loc)
        if area_name in loc:
            if area_name in resp:
                resp[area_name]['income'] = {}
                resp[area_name]['income']['mean'] = int(mean)
                resp[area_name]['income']['median'] = int(median)
            else:
                resp[area_name] = {}
                resp[area_name]['income'] = {}
                resp[area_name]['income']['mean'] = int(mean)
                resp[area_name]['income']['median'] = int(median)

    crime_name = ['Against the person','Property and deception', 'Drug offences', 'Public order and security', 'Justice procedures', 'Other offences']
    for i in range(len(crime)):
        area = crime.loc[i, 'lga_name11']
        value = crime.loc[i, [' total_division_a_offences',' total_division_b_offences',' total_division_c_offences',' total_division_d_offences',' total_division_e_offences',' total_division_f_offences']]
        area_name = wash_lga_name(area, loc)
        if area_name in loc:
            if area_name in resp:
                resp[area_name]['crime'] = {}
                for c in range(6):
                    resp[area_name]['crime'][crime_name[c]] = int(value[c])
            else:
                resp[area_name] = {}
                resp[area_name]['crime'] = {}
                for c in range(6):
                    resp[area_name]['crime'][crime_name[c]] = int(value[c])

    for k,v in resp.items():
        if 'rent' not in v:
            v['rent'] = None
        if 'income' not in v:
            v['income'] = {'mean':None,'median':None}
        if 'crime' not in v:
            v['crime'] = {}
            for c in range(6):
                v['crime'][crime_name[c]] = None

    cdb = CouchDB()
    ic_db = cdb.create_db('area_rent_income_crime')
    ic_db = cdb.get_db('area_rent_income_crime')
    ic_db.save(resp)
    return resp

def save_au_heat():
    cdb = CouchDB()
    au_db = cdb.get_db('has_location_try')
    table = au_db.iterview('_design/dictionary/_view/geo',3000,descending=True)
    resp = {}
    resp = precess_au_heatmap(table)
    with open('au_heatmap_mid.json','w') as jj:
        json.dump(resp, jj)
    ic_db = cdb.create_db('au_heatmap')
    ic_db = cdb.get_db('au_heatmap')
    ic_db['au_heat_new'] = resp
    return resp

def save_area_age():
    age = pd.read_csv('./api/data/age.csv')
    f = open('./api/data/vic_geo.json','r')
    vic = json.load(f)
    f.close()

    loc = []
    for i in vic['features']:
        loc.append(i['properties']['vic_lga__3'])

    aa = []
    for i in range(76):
        if i % 15 == 0:
            if i == 75:
                aa.append('75 +')
            else:
                aa.append('%d - %d' % (i, i+14)) 
    resp = {}
    for i in range(len(age)):
        area = age.loc[i, ' lga_name']
        pop = age.loc[i, [        ' _0_4_yrs_proj_count',   ' _5_9_yrs_proj_count', 
                                ' _10_14_yrs_proj_count', ' _15_19_yrs_proj_count', 
                                ' _20_24_yrs_proj_count', ' _25_29_yrs_proj_count',
                                ' _30_34_yrs_proj_count', ' _35_39_yrs_proj_count',
                                ' _40_44_yrs_proj_count', ' _45_49_yrs_proj_count',
                                ' _50_54_yrs_proj_count', ' _55_59_yrs_proj_count',
                                ' _60_64_yrs_proj_count', ' _65_69_yrs_proj_count',
                                ' _70_74_yrs_proj_count', '_75_79_yrs_proj_count',
                                ' _80_84_yrs_proj_count',' _85_yrs_over_proj_count']]
        
        area_name = wash_lga_name(area,loc)

        if area_name in loc:
            resp[area_name] = {}
            resp[area_name]['data'] = {}
            ge = []
            count = 0
            for i in range(1,len(pop)+1):
                if i % 3 == 0:
                    count += int(pop[i-1])
                    ge.append(count)
                    count = 0
                else:
                    count += int(pop[i-1])
            resp[area_name]['data']['count'] = ge
            resp[area_name]['data']['labels'] = aa


    cdb = CouchDB()
    ric_db = cdb.create_db('area_age')
    ric_db = cdb.get_db('area_age')

    ric_db['age_15'] = resp
    return resp

def save_hotword():
    cdb = CouchDB()
    e_db = cdb.get_db('melbourne20_21')
    h_db = cdb.get_db('abc')
    table = e_db.iterview('_design/dictionary/_view/textdate',10000)
    #timeline = get_topN(table)
    with open('timeline_all_reduce.json','r') as jj:
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
    s_db = cdb.get_db('heatmap_lang')
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
    f = open('has_loc.json', 'r')
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
    s_db = cdb.get_db('heatmap_lang_all')
    for k,v in big_resp.items():
        print(k)
        s_db[k] = v
    return big_resp


def save_lga_tweet():
    cdb = CouchDB()
    s_db = cdb.get_db('sentiment_location')
    table = s_db.view('_design/dictionary/_view/sentiment')
    resp = process_lga_tweet(table)
    result_db = cdb.create_db('lga_tweet')
    result_db = cdb.get_db('lga_tweet')
    result_db['lga'] = resp

