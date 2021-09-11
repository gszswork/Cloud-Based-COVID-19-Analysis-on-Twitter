import json
import sys
from tqdm import tqdm
import jsonlines
import random
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import re

def read_small_json(input_file):
    with open(input_file) as f:
        data = json.load(f)
    return data

def get_word_freq(d, ll):
    sentence_temp = d.copy()
    reg = re.compile(r'[a-z]')
    stopword = set(stopwords.words('english'))
    for word in ll:
        word = word.replace('_', '')
        flag = 0
        #remove stopwords
        if word in stopword:
            flag = 1
            continue
        #remove any word that does not contain any English alphabets
        if not reg.match(word):
            flag = 1
            for c in word:
                if ord(c) >= 97 and ord(c) <= 122: 
                    flag = 0
                    break
        if not flag:
            if word in sentence_temp: sentence_temp[word]+=1
            else: sentence_temp[word] = 1
    
    sentence_temp = dict(sorted(sentence_temp.items(), key=lambda item: item[1],reverse=True))
    new ={}
    c = 0
    for k, v in sentence_temp.items():
        new[k] = v
        c+=1
        if c > 51:
            break
    return new

def read_json_line(input_file, n):
    data = {}
    c = 0
    with jsonlines.open(input_file) as reader:
        for obj in reader:
            if c < n:
                data[c] = obj
                c += 1
            else:
                break
    return data

def read_n_line(n, mode):
    try:
        if int(n) <= 0:
            print('ERROR: Number of line requested must greater than 0!!!')
            return None
        # Opening JSON file
        n = int(n)
        if mode == 'raw':
            data = read_json_line('./backend/api/data/test.data.jsonl', n)
        
        return data
    except:
        print('ERROR: Number of line requested is illegal!!!')
        return None

def get_all_hashtags(data):
    hashtags = {}
    for word, frequency in data.items():
        if word.startswith("#") and len(word) > 1:
            hashtags[word] = frequency
    return dict(sorted(hashtags.items(), key=lambda item: item[1],reverse=True))

def make_name_data(name, data):
    resp = {}
    resp['name'] = name
    resp['data'] = data
    return resp

from datetime import datetime, timedelta

def get_time(elm):
    print(elm[-5:])
    if '-+' in elm:
        date = datetime.strptime(elm, '%a-%b-%d-%H:%M:%S-+0000-%Y')
    elif elm[-5:] == '+0000':
        date = datetime.strptime(elm, '%Y-%m-%d %H:%M:%S+0000')
    else:
        date = datetime.strptime(elm, '%Y/%m/%d/%H')
    return date



def get_front_time(time_str):
    data = datetime.strptime(time_str, '%b-%d-%Y-%H:%M:%S')
    return data

from collections import Counter

def get_top_word_1(l, data,mode = 'word', n = 20):
    total = Counter({})
    for i in tqdm(data.view('_all_docs')):
        if i.id in l:
            w = data.get(i.id)
            w.pop('_id')
            w.pop('_rev')
            word = w['data'].copy()
            total += Counter(word)

    print('finish')
    total = dict(total)
    if 'rt' in total:
        total.pop('rt')
    total = dict(sorted(total.items(), key=lambda item: item[1],reverse=True))
    resp = {'series':[{'data':[]}], 'name':[]}
    c = 1
    if mode == 'word':
        for k, v in total.items():
            resp['series'][0]['data'].append(v)
            resp['name'].append(k)
            if c >= n:
                return resp
            c += 1
    else:
        hash_total = get_all_hashtags(total)
        for k, v in hash_total.items():
            resp['series'][0]['data'].append(v)
            resp['name'].append(k)
            if c > n:
                return resp
            c += 1
    return resp

def generate_data_key(start, end):
    l = []
    delta = timedelta(hours=1)
    start = get_front_time(start)
    end =  get_front_time(end)
    while start < end:
        l.append(start.strftime('%Y/%m/%d/%H'))
        start += delta
    return l


def wash_lga_name(lga_name, real_name):
    dif_len, a_len, b_len = 0,0,0
    lga_name = lga_name.replace('-',' ')
    result_name = '_'
    for name in real_name:
        if name.lower() in lga_name.lower():
            if a_len == 0:
                a_len = len(name)
                b_len = len(lga_name)
                dif_len = abs(a_len - b_len)
                result_name = name
            else:
                a_len = len(name)
                b_len = len(lga_name)
                if abs(a_len-b_len) < dif_len:
                    dif_len = abs(a_len - b_len)
                    result_name = name
    if len(result_name) == 0:
        return lga_name
    else:
        return result_name


def precess_lang(dataset,rname):
    resp = {}

    for index in tqdm(range(len(dataset))):
        area = dataset.loc[index, 'LGA 2011']
        real_name = wash_lga_name(area, rname)
        if real_name in rname:
            if real_name in resp:
                lang_name = dataset.loc[index, 'Language Spoken at Home'].replace('\"','')
                if 'total' in lang_name.lower() or 'other' in lang_name.lower():
                    continue
                if lang_name in resp[real_name]:
                    resp[real_name][lang_name] += int(dataset.loc[index, 'Value'])
                else:
                    resp[real_name][lang_name] = int(dataset.loc[index, 'Value'])
            else:
                resp[real_name] = {}
                lang_name = dataset.loc[index, 'Language Spoken at Home'].replace('\"','')
                if 'total' in lang_name or 'other' in lang_name:
                    continue
                resp[real_name][lang_name] = int(dataset.loc[index, 'Value'])

    return resp
        


def make_geo(loc):
    a = loc.copy()
    a.reverse()
    di = {"type":"Feature","properties":{},"geometry": { "type": "Point"} }
    di["geometry"]["coordinates"] = a
    return di


def precess_case(dataset, loc, rname):
    resp = {"type": "FeatureCollection","features": []}
    for index in range(len(dataset)):
        lga_name = dataset.loc[index, 'Localgovernmentarea']
        real_name = wash_lga_name(lga_name, rname)
        if real_name in loc:
            cord = loc[real_name]
        else:
            cord = loc['Melbourne']
        geo = make_geo(cord)
        resp['features'].append(geo)
    return resp


def random_float(low, high):
    return random.random()*(high-low) + low

def precess_au_heatmap(view, view_16):
    resp = {"type": "FeatureCollection","features": []}
    mem = {}
    for k in tqdm(view):
        v = k['key']
        value = k['value']
        if value not in mem:
            #print(value)
            mem[value] = []

        if v[0]:
            cord = v[0]['coordinates'].copy()
            cord.reverse()
        if v[1]:
            cord = v[1]['coordinates'].copy()
            cord.reverse()

        if v[0] or v[1]:
            mem[value].append(cord)

    for k in view:
        v = k['key']
        value = k['value']
        #print(k)
        if value not in mem:
            #print(value)
            mem[value] = []

        if v[2]:
            sign = random.choice([-1,1])
            if len(mem[value]) > 0:
                cord1 = random.choice(mem[value])
                cord2 = random.choice(mem[value])
                
                if abs(cord1[0] - cord2[0]) < 1:
                    x = random_float(cord1[0], cord2[0])
                else:
                    x = cord1[0] + sign * random_float(0, 0.5)
                sign = random.choice([-1,1])
                if abs(cord1[1] - cord2[1]) < 1:
                    y = random_float(cord1[1], cord2[1])
                else:
                    y = cord1[1] + sign * random_float(0, 0.3)
                #cord = [x,y]
                #dx = random_float(0, 0.01)
                #dy = random_float(0, 0.01)
                #cord = [cord1[0] + dx, cord1[1] + dy]
                cord = [x, y]
            else:
                if abs(v[2][0][0][0] - v[2][0][2][0]) < 0.5:
                    x = random_float(v[2][0][0][0], v[2][0][2][0])
                else:
                    x = v[2][0][0][0] + (v[2][0][2][0] - v[2][0][0][0])/2 + sign * random_float(0,0.3)
                sign = random.choice([-1,1])
                if abs(v[2][0][0][1] - v[2][0][2][1]) < 0.5:
                    y = random_float(v[2][0][0][1], v[2][0][2][1])
                else:
                    y = v[2][0][0][1] + (v[2][0][2][1] - v[2][0][0][1])/2 + sign * random_float(0,0.3)
    
                cord = [y,x]

        if v[0]:
            cord = v[0]['coordinates'].copy()
            cord.reverse()
        if v[1]:
            cord = v[1]['coordinates'].copy()
            cord.reverse()

        if v[0] or v[1]:
            mem[value].append(cord)

        if cord[1] > 142 and cord[1] < 147 and cord[0] > -39 and cord[0] < -36.14:
            print(cord)
            geo = make_geo(cord)
            resp['features'].append(geo)
    
    for t in view_16:
        if t.value:
            cord = t.value.copy()
            cord.reverse()
            geo = make_geo(cord)
            resp['features'].append(geo)
    return resp

def process_lang_heatmap(view):
    resp = {"type": "FeatureCollection","features": []}
    for v in view:
        cord = v.value.copy()
        cord.reverse()
        geo = make_geo(cord)
        resp['features'].append(geo)
    return resp

def stella(resp):
    
    resp.pop('_id')
    resp.pop('_rev')
    new_resp = {}
    for k,v in resp.items():
        new = {'seires':[],'categories' : []}
        data = {'data':[]}
        for lang, count in v.items():
            if count != 0:
                data['data'].append(count)
                new['categories'].append(lang)
        new['seires'].append(data)
        new_resp[k] = new

    return new_resp


def process_sentiment(start, end, sent_db):
    st = get_front_time(start)
    et = get_front_time(end)
    match = [str(st.year), str(st.month), str(st.day), str(st.hour)]
    date = []
    for i in match:
        if len(i) < 2:
            i = '0'+i
        date.append(i)

    if st.year == et.year and st.month==et.month and st.day==et.day:
        score = 0
        c = 1
        hour_table = sent_db.view('_design/dictionary/_view/sentiment', group=True, group_level=4)
        for v in hour_table:
            #print(v.key, date[:-1])
            if v.key[:-1] == date[:-1]:
                if int(v.key[3]) in range(st.hour, et.hour):
                    score += float(v.value['sum'])
                    c += 1
        score = score/c
    elif st.year == et.year and st.month==et.month:
        day_table = sent_db.view('_design/dictionary/_view/sentiment', group=True, group_level=3)
        score = 0
        c = 1
        for v in day_table:
            if v.key[:-1] == date[:-2]:
                if int(v.key[2]) in range(st.day, et.day):
                    score += float(v.value['sum'])/float(v.value['count'])
                    c += 1
        score = score/c
    elif st.year == et.year:
        month_table = sent_db.view('_design/dictionary/_view/sentiment', group=True, group_level=2)
        score = 0
        c = 1
        for v in month_table:
            if v.key[:-1] == date[:-3]:
                if int(v.key[1]) in range(st.month, et.month):
                    score += float(v.value['sum'])/float(v.value['count'])
                    c += 1
        score = score/c
    else:
        year_table = sent_db.view('_design/dictionary/_view/sentiment', group=True, group_level=1)
        score = 0
        c = 1
        for v in year_table:
            if v.key[:-1] == date[:-4]:
                if int(v.key[0]) in range(st.month, et.month):
                    score += float(v.value['sum'])/float(v.value['count'])
                    c += 1
        score = score/c
    return score



def process_lga_tweet(table):
    resp = {}
    covid_keyword = ['covid', 'virus', 'positive', 'case', 'vaccine', 'wuhan', 'lockdown', 'recover','hospital', 'mask', 'lung', 'isola', 'dead', 'death','health','rna','dna','mrna','biontech','pfizer']
    crime_keyword = ['police', 'durg', 'kill','murder','theaf','rob','000','emergency','suspect','catch','caught']
    tt = TweetTokenizer()

    for v in tqdm(table):
        area = v.value
        text = v.key[0].lower()
        score = v.key[1]
        covid_keyword = ['covid', 'virus', 'positive', 'case', 'vaccine', 'wuhan', 'lockdown', 'recover','hospital', 'mask', 'lung', 'isola', 'dead', 'death','health','rna','dna','mrna','biontech','pfizer']
        crime_keyword = ['police', 'durg', 'kill','murder','theaf','rob','000','emergency','suspect','catch','caught']
        if area not in resp:
            resp[area] = {}
            resp[area]['covid_count'] = 0
            resp[area]['tweet_count'] = 0
            resp[area]['crime_count'] = 0
            resp[area]['full_text'] = ''
            resp[area]['hotword'] = {}
            resp[area]['score'] = 0
            resp[area]['c'] = 0

        for key in covid_keyword:
            if key in text:
                resp[area]['covid_count'] += 1
                break
        for key in crime_keyword:
            if key in text:
                resp[area]['crime_count'] += 1
                break
        resp[area]['tweet_count'] += 1
        resp[area]['score'] += score
        if score != 0:
            resp[area]['c'] += 1.0
        word_freq = resp[area]['hotword'].copy()
        ll = [w.lower() for w in tt.tokenize(text)]
        word_freq = get_word_freq(word_freq,ll)
        resp[area]['hotword'] = word_freq.copy()
    
    for lga, info in resp.items():
        info['score'] = info['score']/info['c']
        info.pop('full_text')
        info.pop('c')

    return resp
    

