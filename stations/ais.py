################################################################################
### 1. HEADER                                                                ###
################################################################################
# -*- coding: utf-8 -*-

"""
@authors: Phil Scalabrini & Ysael Desage
"""

################################################################################
### 2. IMPORTS                                                               ###
################################################################################

# GENERAL
import streamlit as st
import os
import pandas as pd
import datetime as dt
from os.path import join
from ais_utils import get_gc1205_lat_lon
import pydeck as pdk


################################################################################
### 3. MAIN CODE                                                             ###
################################################################################

# Note: Pydeck expects lon,lat (X,Y)
def load_ais_data(filename):
    df_in = pd.read_excel(filename, sheet_name='coordonnes')
    points_list = [[df_in.values[i, -1], df_in.values[i, -2]]
                   for i in range(1, len(df_in))
                   if [df_in.values[i, -2], df_in.values[i, -1]] != [df_in.values[i - 1, -2], df_in.values[i - 1, -1]]]
    return points_list

def write(**kwargs):

    # DATA ACQUISITION
    img_col, title_col = st.columns((1, 5))
    img_col.image(join("stations", 'visual_ais.png'))
    title_col.title('AIS')

    coord_boat = get_gc1205_lat_lon()

    df_boat = pd.DataFrame({'lat': [coord_boat[0]], 'lon': [coord_boat[1]]})

    st.header('Informations Actuelles')
    st.write(f"Vitesse: 0 noeuds")
    st.write(f"Orientation: 135º")
    st.map(data=df_boat)

    st.header("Historique")

    st.date_input("Choisir la date", dt.datetime(year=2022, month=6, day=18))
    st.write("Distance parcourue: ", 23, "miles nautiques.")

    points = load_ais_data('ais_data_18_06.xlsx')

    plot_df_dict = {
        'name': ['test_path1'],
        'color': [(255, 166, 26)],
        'path': [points]
    }

    df = pd.DataFrame(plot_df_dict)

    view_state = pdk.ViewState(
        latitude=points[0][1], longitude=points[0][0], zoom=11)

    layer = pdk.Layer(
        type="PathLayer",
        data=df,
        pickable=True,
        get_color="color",
        width_scale=20,
        width_min_pixels=2,
        get_path="path",
        get_width=1,
    )

    r = pdk.Deck(layers=[layer], initial_view_state=view_state,
                 tooltip={"text": "{name}"},
                 map_provider="mapbox",
                 map_style=pdk.map_styles.CARTO_LIGHT)

    st.pydeck_chart(r)

################################################################################
### X. ENF OF CODE                                                           ###
################################################################################
