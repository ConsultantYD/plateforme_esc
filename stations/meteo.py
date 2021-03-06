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
    img_col, title_col = st.columns((1, 5))
    img_col.image(join("stations", 'visual_meteo.png'))
    title_col.title('Meteo')

    coord_base = (46.046528, -73.116527)

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

    st.header("Conditions actuelles")
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
    col01, col02, col03, col04 = st.columns(4)
    T = cond_dict['Temp??rature (C)']
    Humidex = cond_dict["Humidex"] if cond_dict["Humidex"] is not None else T
    dT = round(Humidex - T)
    col01.metric("Temp??rature (??C)", T)
    col02.metric("Humidex", Humidex, dT, delta_color="inverse")
    col03.metric("Vent (km/h)", str(cond_dict["Vitesse de vent (km/h)"]) + ' ' + str(
        cond_dict["Direction de vent"]))
    col04.metric("Indice UV", cond_dict["Indice UV"])
    st.write(cond_dict["Pr??vision"])
    #st.write(cond_dict)

    st.header("Pr??visions ?? court terme (8h)")
    if st.checkbox("Montrer les pr??visions court terme", True):

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
            "temps": t_h_forecast,
            "temperature": temp_h_forecast,
            "precipitations": precip_h_forecast
        })

        # Temperatures
        fig11 = px.line(df.iloc[0:8], x="temps",
                        y="temperature", text="temperature")
        fig11.update_traces(textposition="bottom center", line_color='#ff0000')
        fig11.update_layout({
            "plot_bgcolor": "rgba(0,0,0,0)"
        })
        st.markdown("**Temp??rature**")
        st.plotly_chart(fig11)

        # Pourcentage de pr??cipitations
        fig12 = px.bar(df.iloc[0:8], y='precipitations',
                       x='temps', text='precipitations')
        fig12.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig12.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        fig12.update_layout({
            "plot_bgcolor": "rgba(0,0,0,0)",
            "yaxis_range": [0, 100]
        })
        st.markdown("**Probabilit??s d'averses**")
        st.plotly_chart(fig12, use_container_width=True)

    st.header("Pr??visions ?? long terme (7 jours)")
    if st.checkbox("Montrer les pr??visions long terme"):
        st.write("En d??veloppement.")

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
