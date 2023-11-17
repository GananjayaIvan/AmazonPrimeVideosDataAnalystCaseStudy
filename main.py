import pandas as pd
import json
import plotly.express as px
import numpy as np
from PIL import Image
import streamlit as st
from datetime import datetime, timezone, timedelta
import os


df = pd.read_csv("sample.csv")
df_cekData = df["listed_in"]
df_cekData.to_csv("CekData")
#df["listed_in"] = '"' + df["listed_in"].astype(str) + '"'
#df.to_csv("sample1.csv")

#DataChart1&2
df_ShowTypeDistribution = df.groupby(["type", "release_year"]).size().reset_index(name='total')
#print(df_ShowTypeDistribution)

#DataChart3
df_Content = df.groupby(["type","listed_in"]).size().reset_index(name='total')

#print(df_Content["listed_in"].unique())
df["listed_in"] = df["listed_in"].astype(str)
group_count = df['listed_in'].str.split(expand=True).stack().value_counts()
print(group_count)

column_names=["Genre","Count"]
ArtsEntertainmentCulture = ["Arts", "Entertainment","and"]
group_count=group_count.reset_index()
group_count.rename(columns={"index": "Genre", 0:"Total"}, inplace=True)
group_count["Genre"] = group_count["Genre"].str.replace("^\['|'\]$,","")
group_count["Genre"] = group_count["Genre"].replace(',','', regex=True)
group_count = group_count[group_count["Genre"].str.contains("Arts|Entertainment|and")==False]
group_count["Genre"] = group_count["Genre"].replace('Culture','Arts, Entertainment, and Culture', regex=True)
group_count.groupby(group_count.columns, axis=1).sum()
group_count = group_count.sort_values(by='Total', ascending = False)


#print(group_count.to_csv("test.csv"))
#print(group_count)

#DataChart4&5
dfduration = df.groupby(["duration","type"]).size().reset_index(name='total')
dfduration_show = dfduration[dfduration['type'] == 'TV Show']
dfduration_movies = dfduration[dfduration['type'] == 'Movie']
dfduration_show['duration'] = dfduration_show['duration'].str.replace(' Seasons',"")
dfduration_show['duration'] = dfduration_show['duration'].str.replace(' Season',"").astype(int)
dfduration_movies['duration'] = dfduration_movies['duration'].str.replace(' min',"").astype(int)
dfduration_show = dfduration_show.sort_values(by='duration', ascending = True)
dfduration_movies = dfduration_movies.sort_values(by='duration', ascending = True)

print(dfduration_show)
print(dfduration_movies)

palette = {"Movie": "#0064FF","TV Show":"#FF8FDF"}

TypeRatio = px.pie(df_Content,
    title="Movie/TV Show Ratio",
    values='total',
    names='type',
    color_discrete_sequence=["#83A2FF", "#ED2B2A"
],
)

TypeDistribution = px.bar(df_ShowTypeDistribution,
    title="Type of Show Filtered by Year",
    x='release_year',
    y='total',
    color='type',
    barmode='overlay',
    template='plotly_white',
    labels={
        "release_year": "Release Year",
        "total": "Number of Releases"
                 },
    )

GenreChart = px.histogram(group_count,
    title="Frequency of Genre Listed In Amazon Prime",
    x='Total',
    y='Genre',
    color='Genre',
    template='plotly_white',
    labels={
        "Total": "Genre Counts",
        "Genre": "Types of Genre"
                 },
    ).update_layout(yaxis={'categoryorder':'total ascending'})

DurationChartMovies = px.scatter(dfduration_movies,
    title="Duration of Movies",
    x='duration',
    y='total',
    template='plotly_white',
    labels={
       "duration": "Runtime (in minutes)",
        "total": "Number of Movies"
        },
    ).update_layout(yaxis={'categoryorder':'total ascending'})

DurationChartShow = px.bar(dfduration_show,
    title="Duration of Shows",
    x='duration',
    y='total',
    template='plotly_white',
    labels={
                    "duration": "Runtime (Number of Seasons)",
                    "total": "Number of Show"
                 }
    ).update_layout(yaxis={'categoryorder':'total ascending'})

#RatingChart
TypeRatio.show()
TypeDistribution.show()
GenreChart.show()
DurationChartMovies.show()
DurationChartShow.show()
