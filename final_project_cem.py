"""
Name:       Your Name
CS230:      Section XXX
Data:       Which data set you used
URL:        Link to your web application online (see extra credit)

Description:

This program analyzes the Skyscrapers.csv file. It creates a world map with all of the values using pydeck to be shown on Streamlit.
Next it focuses on making a bar chart taking user input from Streamlit and allows user to customize the chart greatly
Followed by the bar chart, users are allowed to investigate the different type of buildings and it creates a pie chart with the selected value exploded for easier view.

"""
import pandas as pd
import pydeck as pdk
import streamlit as st
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import final_help
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2

#Data Frame
#File Dictionary (Key - Name : Values List - [Feet, Year, Type, Main use, Country, City,lat,lon])
df, file_dict = final_help.read_data('skyscrapers.csv')

#Title
st.title(f"Final Project Cem Ozsumer \n Skyscrapers Around the World")

#Continent Addition to Each Item
i = 0
country_list = []
for country in df.Country:
    a = final_help.get_continent(country)
    country_list.append(a)

    df.loc[i,'Continent'] = a
    i += 1
num = 0
for k in file_dict.keys():
        file_dict[k].append(country_list[num])
        num+=1

#MAP
final_help.world_map(df)

#PLOT 1
st.header("Plot Time!")
options = { "Country": 4,  "Continent": 8, "Year": 1}
left_column, right_column = st.beta_columns(2)
with left_column:
    select = st.radio("Pick an option to use in bar chart: ",list(options.keys()))
with right_column:
    primary = st.color_picker(label = "Pick your primary color")
    secondary = st.color_picker(label = "Pick your secondary color")

bar_info = final_help.freq_dict_function(file_dict, options[select])
sorted_bar_key, sorted_bar_value = final_help.sort_dict_func(bar_info)

grid = st.checkbox(label = "Would you like plot grid?")
if grid:
    left_column, right_column = st.beta_columns(2)
    with left_column:
        grid_color = st.color_picker(label = "Pick your grid color")
    with right_column:

        values = {'Line':'-','Dashed':'--','Dot-dash':'-.','Dotted':':'}
        user_grid = st.selectbox("Pick an option to use in bar chart: ",options = list(values.keys()))
        grid_style = values[user_grid]
    st.pyplot(final_help.bar_chart_plot(sorted_bar_key, sorted_bar_value,select,primary,secondary,grid_color,grid_style))
else:
    st.pyplot(final_help.bar_chart_plot(sorted_bar_key, sorted_bar_value,select,primary,secondary))

#PLOT 2
st.header("Building Type & Pie Chart")
def filterType(df,x):
    return df[df['Type'] == x]

build_list = list(df.Type.unique())
type_select = st.selectbox(label ="Type of Building", options=build_list)
df_type = filterType(df, type_select)
st.dataframe(df_type)

build_num = build_list.index(type_select)

type_all_list = list(df.groupby('Type')['Type'].count())
type_all_list.sort(reverse = True)

st.pyplot(final_help.pie_chart(type_all_list,build_list,build_num))
