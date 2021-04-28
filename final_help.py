import pandas as pd
import pydeck as pdk
import streamlit as st
import numpy as np
#import matplotlib
#import matplotlib.pyplot as plt
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2

def read_data(fileName):
    df = pd.read_csv(fileName)
    file_dict = {}
    file_details =[]
    columns = [ 'Feet', 'Year', 'Type', 'Main use', 'Country', 'City','lat','lon']
    for i, row in df.iterrows():
        sub_list = []
        for col in columns:
            col_no = df.columns.get_loc(col)
            sub_list.append(row[col_no])
        file_details.append(sub_list)
    item = 0
    build_name = df['Name']
    for items in file_details:
        file_dict[build_name[item]] = file_details[item]
        item +=1
    return df, file_dict

def get_continent(col):
    try:
        countryName = str(col).strip()
        cn_a2_code =  country_name_to_country_alpha2(countryName)
    except Exception as e:
        print(e)
        cn_a2_code = 'Unknown'
    try:
        cn_continent = country_alpha2_to_continent_code(cn_a2_code)
    except Exception as e:
        print(e)
        cn_continent = 'Unknown'
    return cn_continent

def world_map(df):
    locations = []
    columns = ['Name','lat','lon']
    for i, row in df.iterrows():
        sub_list = []
        for col in columns:
            col_no = df.columns.get_loc(col)
            sub_list.append(row[col_no])
        locations.append(sub_list)
    map_df = pd.DataFrame(locations, columns =['Name','lat','lon'])

    ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/f/f2/Building_icon.png"
    icon_data = {
        "url": ICON_URL,
        "width": 256,
        "height": 256,
        "anchorY": 256,
    }
    map_df["icon_data"] = None
    for i in map_df.index:
        map_df["icon_data"][i] = icon_data

    view_state = pdk.ViewState(
        latitude=0,
        longitude=0,
        zoom = 0,
        pitch = 0)

    layer = pdk.Layer('IconLayer',
                      data = map_df,
                      get_position='[lon, lat]',
                      get_icon="icon_data",
                      #get_radius = 100,
                      get_size =10,
                      get_scale = 100,
                      get_color=[255,0,255],
                      pickable=True
                      )
    #tool_tip = {'html': 'Name: <br/> {Name}', 'style': {'backgroundColor': 'steelblue', 'color': 'white'}}

    map = pdk.Deck( map_style='mapbox://styles/mapbox/light-v9' , initial_view_state = view_state, layers = [layer], tooltip = {"text": "{Name}"})

    st.pydeck_chart(map)

def freq_dict_function(dict, select):
    dict_freq = {}

    for k in dict.keys():
        if dict[k][select] not in dict_freq.keys():
            item = dict[k][select]
            dict_freq[item] = 1
        else:
            item = dict[k][select]
            dict_freq[item] +=1

    return dict_freq

def sort_dict_func(dict):
    frequency = sorted(dict.values(), reverse= True)
    sorted_dict = {}
    for f in frequency:
        for x in dict.keys():
            if dict[x] == f:
                sorted_dict[x] = dict[x]
                dict.pop(x)
                break
    sorted_key = [key for key in sorted_dict.keys()]
    sorted_freq = [freq for freq in sorted_dict.values()]
    return sorted_key, sorted_freq

def bar_chart_plot(x,y,select,primary,secondary,grid_color='r',grid_style=''):
    fig, ax = plt.subplots()
    width = 0.4
    ax.bar(x, y, width = width , align = 'center', color = primary, linewidth = width*2, edgecolor = secondary)
    #Plot Features
    plt.title(f'Bar Chart of Number of Buildings according to {select}')
    plt.ylabel('Number of Buildings')
    plt.xlabel(select)
    plt.xticks(rotation = 90 )
    plt.grid(color = grid_color, linestyle = grid_style, linewidth = 0.5)

    return plt

def pie_chart(sizes,list,num):
    fig, ax = plt.subplots()
    explode_val = [0,0,0,0,0,0,0]
    explode_val[num] = 0.2
    ax.pie(sizes, labels = list,explode = explode_val, autopct='%1.1f%%', startangle=60)
    ax.axis('equal')
    plt.title("Percentage of Buildings according to type", fontweight = 'bold', fontsize = 10)
    return plt

