"""
@Author: Guangzheng Hu
Student ID: 692277

Description: This file defines Django views that process RESTful data received from the frontend and return coorsponding URLs which contians retrieved JSON data.
"""
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
import ujson
import json
from api.toolFunc import *
import couchdb
from couchDbHandler import *
import pandas as pd

# Create your views here.
print('http://127.0.0.1:8000/api/test/3')
def get_n_tweet(request, n):
    if request.method == 'GET':
        resp = read_n_line(n, 'raw')
        if resp:
            return HttpResponse(ujson.dumps(resp), content_type='application/json')
        else:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')


print('http://127.0.0.1:8000/api/death/all')
def get_death_number(request, month):
    if request.method == 'GET':
        resp = {'series': []}
        try:
            cdb = CouchDB()
            death_db = cdb.get_db('death')
            if death_db:
                data = death_db['20f65008d43b65f035c3fc6f4a2399c6']
                d = {}
                if month == 'all':
                    for k, v in data.items():
                        if k != 'category' and k[0] != '_':
                            d['name'] = k
                            d['data'] = v
                            resp['series'].append(d)
                            d = {}

                elif month in data['category']:
                    m = data['category'].index(month)
                    for k, v in data.items():
                        if k != 'category' and k[0] != '_':
                            d['name'] = k
                            d['data'] = v[m]
                            resp['series'].append(d)
                            d = {}
                else:
                    resp = None
        
        except Exception:
            resp = None

        if resp:
            print(ujson.dumps(resp))
            return HttpResponse(json.dumps(resp), content_type='application/json')
        else:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be GET')




print('http://127.0.0.1:8000/api/employment')
def get_employment(request):
    if request.method == 'GET':
        try:
            cdb = CouchDB()
            e_db = cdb.get_db('employment')
            data = e_db['20f65008d43b65f035c3fc6f4a23ccec']
            resp = data
            if resp:
                return HttpResponse(ujson.dumps(resp), content_type='application/json')
            else:
                return HttpResponseBadRequest(resp)
        except Exception:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')

print('http://127.0.0.1:8000/api/tweet/top/word/20/Oct-12-2020-00:00:00/Oct-13-2020-00:00:00')
def get_top(request, mode = 'word', n = 20, timeS = None, timeE=None):
    if request.method == 'GET':
        try:
            cdb = CouchDB()
            data = cdb.get_db('hotword_all')
            sent_db = cdb.get_db('sentiment_analysis')
            l = generate_data_key(timeS,timeE)
            print('here')
            resp = get_top_word_1(l,data, mode, n)
            resp['sentiment_score'] = process_sentiment(timeS, timeE, sent_db)
            if resp:
                return HttpResponse(ujson.dumps(resp), content_type='application/json')
            else:
                return HttpResponseBadRequest(resp)
        except Exception:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')



def get_cases(request):
    if request.method == 'GET':
        try:
            cdb = CouchDB()
            db = cdb.get_db('cases')
            resp = db.get('dc03849c597d859fe1dbe170262687d0')
            if resp:
                resp.pop('_id')
                resp.pop('_rev')
                return HttpResponse(ujson.dumps(resp), content_type='application/json')
            else:
                return HttpResponseBadRequest(resp)
        except Exception:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')


print('http://127.0.0.1:8000/api/language')
def get_lang(request):
    if request.method == 'GET':
        try:
            cdb = CouchDB()
            db = cdb.get_db('language')
            resp = db.get('7c78cc675e58cf2a48b4bd9093e153ff')
            resp = stella(resp)

            if resp:
                return HttpResponse(json.dumps(resp), content_type='application/json')
            else:
                return HttpResponseBadRequest(resp)
        except Exception:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')


print('http://127.0.0.1:8000/api/area/info')
def get_areaInfo(request):
    if request.method == 'GET':
        try:
            print('here')
            cdb = CouchDB()
            db = cdb.get_db('area_rent_income_crime')
            resp = db.get('bdb85cf015fe7fe55ca28dd28cd3f2f4')
            if resp:
                resp.pop('_id')
                resp.pop('_rev')
                return HttpResponse(json.dumps(resp), content_type='application/json')
            else:
                return HttpResponseBadRequest(resp)
        except Exception:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')

print('http://127.0.0.1:8000/api/area/age')
def get_areaAge(request):
    if request.method == 'GET':
        try:
            cdb = CouchDB()
            db = cdb.get_db('area_age')
            resp = db.get('age_15')
            if resp:
                resp.pop('_id')
                resp.pop('_rev')
                return HttpResponse(json.dumps(resp), content_type='application/json')
            else:
                return HttpResponseBadRequest(resp)
        except Exception:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')

print('http://127.0.0.1:8000/api/language/heatmap/en')
def get_langHeat(request, lang):
    if request.method == 'GET':
        try:
            cdb = CouchDB()
            db = cdb.get_db('heatmap_lang_all')
            if lang not in db:
                return HttpResponseBadRequest('language not exist')
            resp = db.get(lang)
            if resp:
                resp.pop('_id')
                resp.pop('_rev')
                return HttpResponse(json.dumps(resp), content_type='application/json')
            else:
                return HttpResponseBadRequest(resp)
        except Exception:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')


print('http://127.0.0.1:8000/api/area/tweet')
def get_areaTweet(request):
    if request.method == 'GET':
        try:
            cdb = CouchDB()
            db = cdb.get_db('lga_tweet_info')
            resp = db.get('lga')
            
            resp.pop('_id')
            resp.pop('_rev')
            for k,v in resp.items():
                h = v['hotword'].copy()
                v['hotword'] = list(h.keys())[:5]
            if resp:
                return HttpResponse(json.dumps(resp), content_type='application/json')
            else:
                return HttpResponseBadRequest(resp)
        except Exception:
            return HttpResponseBadRequest(resp)
    else:
        return HttpResponseBadRequest('request should be get')
