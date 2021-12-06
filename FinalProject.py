import numpy as np
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.api.types import is_numeric_dtype
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import streamlit as st
st.set_page_config(layout="wide")

st.title("Math 10: Final Project")

st.write("This dataset shows us different statistics for shows on different streaming platforms.")

df = pd.read_csv("/Users/Vianey/Downloads/tv_shows.csv", na_values = "")
df



st.write("We will remove the 'Unnamed: 0' and 'Type' columns as they are uneccessary for our purposes, remove any rows that are missing values, and change the values in the 'Age' column to show 'Min Age' instead.")
df1 = df.drop(["Unnamed: 0"], axis = 1)
df1 = df1.drop(["Type"], axis = 1)
df1.dropna(subset = ["IMDb", "Rotten Tomatoes","Age"], inplace = True) 
df1['Age'] = df1['Age'].replace(['4+'], '4')
df1['Age'] = df1['Age'].replace(['16+'], '16')
df1['Age'] = df1['Age'].replace(['18+'], '18')
df1['Age'] = df1['Age'].replace(['7+'], '7')
df1['Age'] = df1['Age'].replace(['all'], '0')
df1['Age'] = df1['Age'].replace(['<NA>'], '0')
df1 = df1.rename(columns = {"Age":"Min Age"})
df1


st.write("Next we will rewrite the ratings in the 'IMDb' and 'Rotten Tomatoes' columns as percentages.")
#Splits string into two parts by numerator and denominator, then use lambda to properly calculate the decimal value 
# of the fraction.

df1["IMDb"] = df1["IMDb"].str.split("/").apply(lambda x: float(x[0])*10) 
df1["Rotten Tomatoes"] = df1["Rotten Tomatoes"].str.split("/").apply(lambda x: float(x[0]) ) 
df1



st.write("Now we will create new columns calculating the 'Average Rating' between IMDb and Rotten Tomatoes, and the 'Total Services' the show is available on.") 
df1["Average Rating"] = df1[['IMDb','Rotten Tomatoes']].mean(axis = 1)
df1.sort_values(by="Average Rating", ascending = False)
df1["Total Services"] = df1[["Netflix","Hulu","Prime Video","Disney+"]].sum(axis = 1)
df1

st.title("Choose a rating to see which shows have that average or higher:")

#Gives new df only containing shows with an average rating greater than or equal to 70%
A = st.slider("Average Rating:",1,100)
df_chosen = df1[df1['Average Rating'] >= A]
bar = alt.Chart(df_chosen).mark_bar().encode(
    x = "Title",
    y = "Average Rating",
    color= "ID",
)
bar

st.write("We can see that Breaking Bad has the highest ratings.")

st.title("Select a part of the scatterplot to see how many services a show is offered on")

select = alt.selection(type='interval')
values = alt.Chart(df1).mark_point().encode(
    x='ID:Q',
    y='Average Rating:Q',
    color=alt.condition(select, 'Total Services:N', alt.value('plasma'))
).add_selection(
    select
)
bars = alt.Chart(df1).mark_bar().encode(
    y='Total Services:N',
    color='Total Services:N',
    x='count(Total Services):Q'
).transform_filter(
    select
)
values & bars





st.write("References:")
st.markdown("[This dataset was taken from here.](https://www.kaggle.com/ruchi798/tv-shows-on-netflix-prime-video-hulu-and-disney)")
st.markdown("[The scatterplot was taken from here.](https://www.analyticsvidhya.com/blog/2021/10/exploring-data-visualization-in-altair-an-interesting-alternative-to-seaborn/)")





