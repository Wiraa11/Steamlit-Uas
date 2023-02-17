from itertools import chain
from streamlit_lottie import st_lottie_spinner
from streamlit_lottie import st_lottie
import requests
import time
import streamlit as st
import altair as alt
import pandas as pd
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(
    layout='wide',
    initial_sidebar_state='collapsed',
    page_title="Visdat ",
    page_icon="📊",)

# 2. horizontal menu
page = option_menu(None, ["Home", "Data", "Visualization"],
                   icons=['house', 'activity', "bar-chart-line"],
                   menu_icon="cast", default_index=0, orientation="horizontal")

data = pd.read_csv('indonesian_movies.csv')
# nRow, nCol = data.shape

# Data Filtered Clean
data = data.dropna(subset=['genre', 'directors'])
data = data.reset_index(drop=True)

data['rating'] = data['rating'].fillna("Unrated")
data['rating'] = data['rating'].replace({
    "Not Rated": "Unrated",
    "R": "13+",
    "PG-13": "13+",
    "TV-14": "13+",
    "TV-MA": "17+",
    "D": "17+",
    "21+": "17+"
})

data["runtime"] = data["runtime"].fillna("90")
data["runtime"] = data["runtime"].apply(lambda x: x.replace(" min", ""))
data["runtime"] = data["runtime"].astype(int)
data["users_rating"] = data["users_rating"].astype(str)

#
if page == "Home":
    # Loading
    my_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete)
    my_bar.empty()

    # with st.expander('About this app'):

    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_url_hello = "https://assets10.lottiefiles.com/packages/lf20_rrqimc3f.json"
    lottie_hello = load_lottieurl(lottie_url_hello)

    # Center Image
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write('')
    with col2:
        # st.image(
        #     'https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png', width=250)
        st.write()
    with col3:

        st_lottie(lottie_hello, key="hello", width=300)
    with col4:
        st.write('')
    with col5:
        st.write('')

    st.markdown("<h1 style='text-align: center; color: black; font-weight: bold'>UAS VISUALISASI DATA</h1>",
                unsafe_allow_html=True)
    st.markdown("# KELOMPOK 4")
    st.markdown("ANGGOTA : \n ")
    st.markdown("Muhamad Attar Ramadhani (09040620058) ")
    st.markdown("Athalia Diah Rizqullah (09020620024)")
    st.markdown("Satria Wira Bakti (09040620066)")


if page == "Data":
    st.header("Data Frame")
    # Filter by Year
    slider = st.slider("Filter by Year : ", 1926, 2020)
    filtered_column1 = data[data['year'] == slider]
    st.dataframe(filtered_column1)

    x = filtered_column1.groupby('year').count()
    var1 = x.rename(columns={"title": "Total Film"})
    var2 = var1['Total Film']
    st.write(var2)

    # Filter by Genre
    genre = st.selectbox("Genre", data["genre"].unique())
    g = data[data["genre"] == genre]
    st.dataframe(g)

    x = g.groupby('genre').count()
    var1 = x.rename(columns={"title": "Total Film"})
    var2 = var1['Total Film']
    st.write(var2)

    # ALL DATA
    data_all = data
    show_data = st.checkbox("Show All Data")
    if show_data:
        st.dataframe(data_all)
        # x = data_all.groupby('year').count()
        # y = x.iloc[0].sum()
        # var1 = x.rename(columns={"title": "Total Film"})
        # var2 = var1['Total Film']
        # var3 = var2.iloc[1].sum()
        # st.write(var2)

    # cek
    # genre = st.write("Kategori", data.genre.unique())

if page == "Visualization":
    st.title("Data Visualization")
    dt = ['visualisasi 1', 'visualisasi 2',
          'visualisasi 3', 'visualisasi 4', 'visualisasi 5']
    terpilih = st.selectbox("pilih ", dt)

    # st.title("Hasil")
    # data["year"] = data["year"].astype(float)
    if terpilih == "visualisasi 1":
        st.write("Jumlah Produksi Film per Tahun")
        valueCounts = data["year"].value_counts()
        st.bar_chart(valueCounts)

    elif terpilih == "visualisasi 2":
        st.write("Jumlah Produksi Film per Tahun berdasarkan genre yang dipilih")
        genre = st.selectbox("Genre", data["genre"].unique())
        x = data[data["genre"] == genre]

        year_count = x.groupby("year").count()["title"]
        st.bar_chart(year_count)

        xx = x.groupby('genre').count()
        var1 = xx.rename(columns={"title": "Total Film"})
        var2 = var1['Total Film']
        st.dataframe(var2)

    elif terpilih == "visualisasi 3":
        st.write("Jumlah Produksi Film per Tahun berdasarkan rating yang dipilih")
        aa = st.selectbox("Rating", data["rating"].unique())
        d = data[data["rating"] == aa]

        a = d.groupby("genre").count()["title"]
        st.bar_chart(a)

        xx = d.groupby('rating').count()
        var1 = xx.rename(columns={"title": "Total Film"})
        var2a = var1['Total Film']
        st.dataframe(var2a)

    elif terpilih == "visualisasi 4":
        st.write("Sutradara Dengan Film Terbanyak ")
        year = st.selectbox("Genre", data["genre"].unique())
        x = data[data["genre"] == year]

        year_count = x.groupby("directors").count()["title"]
        st.bar_chart(year_count)

        xx = x.groupby('genre').count()
        var1 = xx.rename(columns={"title": "Total Film"})
        var2 = var1['Total Film']
        st.dataframe(var2)

        ax = data["directors"].value_counts()[:15]
        st.bar_chart(ax)

    elif terpilih == "visualisasi 5":
        st.write("Pemain Dengan Film Terbanyak ")
        year = st.selectbox("Rating", data["rating"].unique())
        xp = data[data["rating"] == year]

        actors = data["actors"].apply(np.array)
        actorlist = pd.Series(list(chain.from_iterable(
            x.title().split(', ') for x in actors.str[1:-1])))
        actorlist = actorlist[actorlist.str.contains("'")]
        actorlist = actorlist.str.strip("'")
        a = actorlist.value_counts()[:10]
        aa = xp.groupby(actorlist).count()["rating"]
        st.bar_chart(aa)

        st.bar_chart(a)

    else:
        st.write("Anda tidak memilih kategori yang tersedia.")
