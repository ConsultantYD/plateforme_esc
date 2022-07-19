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
import plotly.express as px

import asyncio

from env_canada import ECWeather

from os.path import isfile, join

################################################################################
### 3. MAIN CODE                                                             ###
################################################################################


def write(data_dict: dict, **kwargs):

    # DATA ACQUISITION
    st.title('Meteo')
    img_col, _, _ = st.columns((1, 4, 4))
    img_col.image(join("stations", 'visual_meteo.png'))

    coord_base = (46.046528, -73.116527)
    coord_boat = (46.047640, -73.116527)

    ec_fr = ECWeather(coordinates=coord_base, language='french')

    asyncio.run(ec_fr.update())

    # WeatherCan Raw Format
    alerts = ec_fr.alerts
    cond = ec_fr.conditions
    h_frcst = ec_fr.hourly_forecasts

    # CURRENT CONDITIONS
    # Metrics
    cond_dict = {}
    for k, v in cond.items():
        if 'unit' in v.keys():
            cond_dict[v["label"] + ' (' + v["unit"] + ')'] = v["value"]
        else:
            cond_dict[v["label"]] = v["value"]

    st.subheader("Conditions actuelles")
    # Alerts
    alrt_count = 0
    for k, v in alerts.items():
        if len(v["value"]) > 0:
            for a in range(len(v["value"])):
                st.write(v["label"] + ": " + v["value"][a]["title"])
            alrt_count += 1
    if alrt_count == 0:
        st.write("Aucune alertes.")
    #st.write(alerts)

    # Metrics
    col01, col02, col03, col04, col05, _ = st.columns((1, 1, 1, 1, 1, 2))
    T = cond_dict['Température (C)']
    Humidex = cond_dict["Humidex"] if cond_dict["Humidex"] is not None else T
    dT = round(Humidex - T)
    col01.metric("Température (ºC)", T)
    col02.metric("Humidex", Humidex, dT, delta_color="inverse")
    col03.metric("Vent (km/h)", str(cond_dict["Vitesse de vent (km/h)"]) + ' ' + str(
        cond_dict["Direction de vent"]))
    col04.metric("Indice UV", cond_dict["Indice UV"])
    st.write(cond_dict["Prévision"])
    #st.write(cond_dict)

    st.subheader("Prévisions à court terme (8h)")
    if st.checkbox("Montrer les prévisions court terme", True):
        col11, col12, _ = st.columns((3, 3, 1))

        # Forecast (hourly)
        t_h_forecast = []
        temp_h_forecast = []
        precip_h_forecast = []

        for i in h_frcst:
            temp_h_forecast.append(i["temperature"])
            precip_h_forecast.append(i["precip_probability"])
            t_h_forecast.append(i["period"] - dt.timedelta(hours=4))

        t_h_forecast = np.array(t_h_forecast)
        temp_h_forecast = np.array(temp_h_forecast)
        precip_h_forecast = np.array(precip_h_forecast)
        #precip_h_forecast = np.random.uniform(0, 1, size=24) * 100
        #precip_h_forecast = np.round(precip_h_forecast, 2)
        df = pd.DataFrame({
            "time": t_h_forecast,
            "temperature": temp_h_forecast,
            "precipitations": precip_h_forecast
        })

        # Temperatures
        fig11 = px.line(df.iloc[0:8], x="time",
                        y="temperature", text="temperature")
        fig11.update_traces(textposition="bottom center", line_color='#ff0000')
        fig11.update_layout({
            "plot_bgcolor": "rgba(0,0,0,0)"
        })
        col11.markdown("**Température**")
        col11.plotly_chart(fig11)

        # Pourcentage de précipitations
        fig12 = px.bar(df.iloc[0:8], y='precipitations',
                       x='time', text='precipitations')
        fig12.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig12.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        fig12.update_layout({
            "plot_bgcolor": "rgba(0,0,0,0)",
            "yaxis_range": [0, 100]
        })
        col12.markdown("**Probabilités d'averses**")
        col12.plotly_chart(fig12, use_container_width=True)

    st.subheader("Prévisions à long terme (7 jours)")
    if st.checkbox("Montrer les prévisions long terme"):
        st.write("En développement.")

    """
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
    col2.subheader("Hourly Forecasts")
    col2.write()

    print(ec_fr.alerts)

    #cond = pd.DataFrame(ec_fr.conditions)
    #st.write(cond)
    """

################################################################################
### X. END OF CODE                                                           ###
################################################################################
