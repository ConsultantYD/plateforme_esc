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

from os.path import isfile, join

################################################################################
### 3. MAIN CODE                                                             ###
################################################################################


def write(data_dict: dict, **kwargs):

    # DATA ACQUISITION
    st.title('Meteo')
    st.info("Cette page est en cours de développement.")

    coord_base = (46.046528, -73.116527)
    coord_boat = (46.047640, -73.116527)

    ec_fr = ECWeather(coordinates=coord_base, language='french')

    asyncio.run(ec_fr.update())

    cond = ec_fr.conditions
    cond_dict = {}
    for k, v in cond.items():
        if 'unit' in v.keys():
            cond_dict[v["label"] + ' (' + v["unit"] + ')'] = v["value"]
        else:
            cond_dict[v["label"]] = v["value"]

    col1, col2, _ = st.columns((2, 2, 1))
    col1.header("Base")
    col1.subheader("Alertes")
    col1.write({})
    col1.subheader("Conditions")
    col1.write(cond_dict)
    col2.header("Bateau")
    col2.subheader("Alertes")
    col2.write({})
    col2.subheader("Conditions")
    col2.write(cond_dict)

    print(ec_fr.alerts)

    #cond = pd.DataFrame(ec_fr.conditions)
    #st.write(cond)

################################################################################
### X. END OF CODE                                                           ###
################################################################################
