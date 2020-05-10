# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 13:07:39 2020

@author: SURIMWANG
"""

#%%
import glob
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import platform 
from matplotlib  import font_manager, rc


plt.rcParams['axes.unicode_minus']= False 
if platform.system() == 'Darwin': 
    rc('font', family = 'AppleGothic') 
elif platform.system() =='Windows': 
    path = "C:/Windows/Fonts/malgun.ttf" 
    font_name = font_manager.FontProperties(fname=path).get_name() 
    rc('font', family = font_name) 
else: 
    print('Unknown system... sorry~~~~') 

%matplotlib inline

#%%

data = pd.read_excel('../../data/00.도로_국가소음정보시스템.xlsx')

data = data.drop(['Unnamed: 0', '도시_x', '용도구분_x'], axis = 1)

data.columns = ['측정지점', '년도', '반기', '8시', '16시', '낮평균', '23시', '도시', '용도구분', '측정지역']

len(data.측정지점.unique())
data.측정지점.unique()

data['검색키워드'] = data.측정지역 + data.측정지점
#%%
import googlemaps
gmaps_key = 'AIzaSyAiVnaefWdlnEWEbkmAkrT408Jd7OhPbHA'
gmaps = googlemaps.Client(key=gmaps_key)


lat_lst= []
lng_lst= []
for name in data.검색키워드:
    tmp = gmaps.geocode(name, language= 'ko')
    tmp_loc = tmp[0].get("geometry")    
    lat = tmp_loc['location']['lat']    
    lng = tmp_loc['location']['lng']    
    lat_lst.append(lat)
    lng_lst.append(lng)    


data['lat'] = lat_lst
data['lng'] = lng_lst


#%%
###
import json
geo_path = '../../data/02. skorea_municipalities_geo_simple.json'
geo_str = json.load(open(geo_path, encoding='utf-8'))

import folium


###
map = folium.Map(location=[37.5502,126.982], zoom_start =10) # tiles='Stamen Toner'

for i in data['lat'].index:
    folium.Marker(location = [data['lat'][i], data['lng'][i]], 
                  popup=[data['측정지점'][i], data['낮평균'][i]],
                  icon=folium.Icon(color='green', icon = 'ok')
                 ).add_to(map)
#location = [crime_anal_raw['lat'][i],crime_anal_raw['lng'][i]]
  
map.save('../../data/소음/load_map.html')
type(map)
map

data.to_csv('../../data/00.도로_국가소음정보시스템_위경도추가.csv')


























