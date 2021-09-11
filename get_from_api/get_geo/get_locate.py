#this code is used to get lat and lng information from the google api

# Author: yalan zhao
# Student id: 1047739
# Team: COMP90024 - team 24

import json
import sys
import requests
locs = ['Alpine',
 'Ararat',
 'Ballarat',
 'Banyule',
 'Bass Coast',
 'Baw Baw',
 'Bayside',
 'Benalla',
 'Boroondara',
 'Brimbank',
 'Buloke',
 'Campaspe',
 'Cardinia',
 'Casey',
 'Central Goldfields',
 'Colac-Otway',
 'Corangamite',
 'Darebin',
 'East Gippsland',
 'Frankston',
 'Gannawarra',
 'Glen Eira',
 'Glenelg',
 'Golden Plains',
 'Greater Bendigo',
 'Greater Dandenong',
 'Greater Geelong',
 'Greater Shepparton',
 'Hepburn',
 'Hindmarsh',
 'Hobsons Bay',
 'Horsham',
 'Hume',
 'Indigo',
 'Kingston',
 'Knox',
 'Latrobe',
 'Loddon',
 'Macedon Ranges',
 'Manningham',
 'Mansfield',
 'Maribyrnong',
 'Maroondah',
 'Melbourne',
 'Melton',
 'Mildura',
 'Mitchell',
 'Moira',
 'Monash',
 'Moonee Valley',
 'Moorabool',
 'Moreland',
 'Mornington Peninsula',
 'Mount Alexander',
 'Moyne',
 'Murrindindi',
 'Nillumbik',
 'Northern Grampians',
 'Port Phillip',
 'Pyrenees',
 'Queenscliffe',
 'South Gippsland',
 'Southern Grampians',
 'Stonnington',
 'Strathbogie',
 'Surf Coast',
 'Swan Hill',
 'Towong',
 'Wangaratta',
 'Warrnambool',
 'Wellington',
 'West Wimmera',
 'Whitehorse',
 'Whittlesea',
 'Wodonga',
 'Wyndham',
 'Yarra',
 'Yarra Ranges',
 'Yarriambiack']
num=0
ans={}
for loc in locs:
    try:
             request = ('https://maps.googleapis.com/maps/api/geocode/json?address='
                     + loc+',VIC' +',AU'+ '&key=AIzaSyDLyQLWVoJpRYadYLuIffczAYjmr3CCvo0')
             response = requests.get(request)
             response.raise_for_status()
             num += 1
             print('HTTP request successed!--{}'.format(num))
    except Exception as e:
             print('HTTP request failed!-{}'.format(str(e)))
    print(json.loads(response.text)['results'][0]['address_components'][1]['short_name'],json.loads(response.text)['results'][0]['address_components'][2]['short_name'])
    lat = json.loads(response.text)['results'][0]['geometry']['location']['lat']
    lng = json.loads(response.text)['results'][0]['geometry']['location']['lng']
    ans[loc]=[lat,lng]
import json
jsObj = json.dumps(ans)
fileObject = open('locations.json', 'w')
fileObject.write(jsObj)
fileObject.close()
import couchdb
server = couchdb.Server('http://admin:admin@172.26.134.73:5984/')
db = server['australia_location']
db.save(ans)
