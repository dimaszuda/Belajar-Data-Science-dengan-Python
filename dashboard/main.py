import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

dataframe = pd.read_csv('day.csv', delimiter=',')


def tenant(dataframe):
    springer = dataframe[dataframe['season'] == 1]
    summer = dataframe[dataframe['season'] == 2]
    fall = dataframe[dataframe['season'] == 3]
    winter = dataframe[dataframe['season'] == 4]
    total_tenant = [springer['cnt'].sum(), summer['cnt'].sum(),
                    fall['cnt'].sum(),  winter['cnt'].sum()]
    return total_tenant


def trend(dataframe, window_size=30):
    tenant = dataframe['cnt']
    window_size = window_size
    i = 0
    moving_averages = []
    while i < len(tenant) - window_size + 1:
        window_average = round(np.sum(tenant[
            i:i+window_size]) / window_size, 2
        )
        moving_averages.append(window_average)
        i += 1
    return moving_averages


def indice_season(dataframe):
    indices_season = []
    indices_prev_season, prev_season = 0, 1
    for i, season in enumerate(dataframe['season']):
        if season != prev_season:
            indices_season.append([indices_prev_season, i])
            prev_season = season
            indices_prev_season = i+1
    return indices_season


def vis_musim(dataframe):
    total_tenant = tenant(dataframe)
    moving_averages = trend(dataframe, window_size=30)
    indices_season = indice_season(dataframe)
    legend = ['trend', 'Musim Semi', 'Musim Panas',
              'Musim Gugur', 'Musim Dingin']
    season = ['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin']
    seasonCode = [125, 300, 475, 675]

    plt.style.use("ggplot")
    fig, ax = plt.subplots(2, 1, figsize=(20, 14))
    bars = ax[0].bar(seasonCode, total_tenant, width=80,
                     color='#A6FF96', alpha=0.5)
    ax[0].set_title("Visualisasi jumlah penyewa bergantung pada musim",
                    fontsize=30, fontweight='bold')
    ax[0].set_ylabel("Total Jumlah Penyewa", fontsize=18, fontweight='bold')
    ax[0].set_xticks(seasonCode)
    ax[0].set_xticklabels(season, fontsize=18, fontweight='bold')
    max_index = total_tenant.index(max(total_tenant))
    bars[max_index].set_color('#16FF00')

    for bar in bars:
        height = bar.get_height()
        ax[0].annotate(f'{int(height)}',
                       xy=(bar.get_x() + bar.get_width() / 2, height-9000),
                       xytext=(0, 3),
                       textcoords="offset points",
                       fontsize=14,
                       ha='center', va='bottom')

    ax[1].plot(dataframe['instant'][0:len(moving_averages)],
               moving_averages, linewidth=2, color='red')
    ax[1].set_xlabel("Recorded day", fontsize=18, fontweight='bold')
    ax[1].set_ylabel("Jumlah Penyewa", fontsize=18, fontweight='bold')

    colors = ['green', '#2B3A55', 'blue', 'yellow']
    c = 0
    for val in indices_season:
        i, j = val
        color = colors[c]
        ax[1].axvspan(i, j, color=color, alpha=0.3)
        if color == "yellow":
            c = -1
        c += 1
    plt.legend(legend, loc='upper center', fontsize=15)
    return fig

# create visualization function


def vis(dataframe, filt, data, Code, explode, title):
    pie_result = dataframe.groupby(filt)['cnt'].sum().tolist()
    data = data
    Code = Code

    fig, ax = plt.subplots(1, 2, figsize=(
        20, 14), gridspec_kw={'width_ratios': [2, 3]})
    bars = ax[0].bar(data, pie_result, color='#186F65')
    ax[0].set_xticks(data)
    ax[0].set_xticklabels(Code, fontsize=21, fontweight='bold')

    for bar in bars:
        height = bar.get_height()
        ax[0].annotate(f'{int(height)}',
                       xy=(bar.get_x() + bar.get_width() / 2, height-9000),
                       xytext=(0, 3),
                       textcoords="offset points",
                       fontsize=20,
                       ha='center', va='bottom')

    explode = explode

    pie_result, texts, autotexts = ax[1].pie(
        pie_result,
        labels=Code,
        autopct='%1.2f%%',
        colors=['#186F65', '#FFA33C'],
        explode=explode,
        startangle=110,
        labeldistance=0.35,
        pctdistance=0.7)

    for t in texts:
        t.set_fontsize(20)
        t.set_color('white')
        t.set_fontweight('bold')

    for text in autotexts:
        text.set_fontsize(20)
        text.set_color('white')
        text.set_fontweight('bold')

    plt.axis('equal')

    fig.suptitle(title, fontsize=29, fontweight='bold')
    return fig


workingDay = vis(dataframe,
                 'workingday',
                 data=[0, 1],
                 Code=['Holiday', 'Workingday'],
                 explode=(0, 0.1),
                 title='Jumlah Penyewa Sepeda berdasarkan hari kerja'
                 )
weather = vis(dataframe,
              'weathersit',
              data=[1, 2, 3],
              Code=['Clear', 'Cloudy', 'Light Rain'],
              explode=None,
              title='Jumlah Penyewa Sepada berdasarkan Musim')

st.title('Dicoding Submission - Explore Insight on Bicycle Sharing System')
st.caption('Nama: Dimas Zuda Fathul Akhir')
st.caption('Email: dimas.zuda45@gmail.com')

df, visualize = st.tabs(['DataFrame', 'Visualisasi'])

list = {'Musim', 'Hari Kerja', 'Cuaca'}
with df:
    st.write("This is the dataset of the Daily Bike Sharing")
    st.dataframe(dataframe)

with visualize:
    option = st.selectbox(
        'Gain Insight',
        options=list
    )
    if option == 'Musim':
        fig = vis_musim(dataframe)
        st.pyplot(fig)
    elif option == 'Hari Kerja':
        st.pyplot(workingDay)
    else:
        st.pyplot(weather)
