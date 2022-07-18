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
import pandas as pd
import numpy as np
import os
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns

import asyncio

from env_canada import ECWeather
from env_canada import ECHistorical, get_historical_stations

from os.path import isfile, join

################################################################################
### 3. MAIN CODE                                                             ###
################################################################################


def write(data_dict: dict, **kwargs):

    # DATA ACQUISITION
    st.title('Journal de bord')
    img_col,_,_ = st.columns((1,4,4))
    img_col.image(join("stations",'visual_jb.png'))
    st.info("Cette page est en cours de développement.")

    coord_base = (46.046528, -73.116527)
    coord_boat = (46.047640, -73.116527)

    ec_fr = ECWeather(coordinates=coord_base, language='french')

    asyncio.run(ec_fr.update())

    """
    stations = asyncio.run(get_historical_stations(
        coord_base, radius=50, limit=25))

    st.write(stations)

    ec_fr_csv = ECHistorical(station_id=10975, year=2022,
                             language="french", format="csv")

    asyncio.run(ec_fr_csv.update())

    # metadata describing the station
    #st.write(ec_fr_xml.metadata)

    # historical weather data, in dictionary form
    #st.write(ec_fr_xml.station_data)

    # csv-generated responses return csv-like station data
    df = pd.read_csv(ec_fr_csv.station_data)
    st.write(df)
    """

    cond = ec_fr.conditions
    cond_dict = {}
    for k, v in cond.items():
        if 'unit' in v.keys():
            cond_dict[v["label"] + ' (' + v["unit"] + ')'] = v["value"]
        else:
            cond_dict[v["label"]] = v["value"]

    st.write(cond_dict)

    # daily forecasts
    #st.write(ec_fr.daily_forecasts)

    # hourly forecasts
    st.write(ec_fr.hourly_forecasts)

    #cond = pd.DataFrame(ec_fr.conditions)
    #st.write(cond)

################################################################################
### X. END OF CODE                                                           ###
################################################################################
