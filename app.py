################################################################################
### 1. HEADER 																 ###
################################################################################
# -*- coding: utf-8 -*-

"""
@author: Ysael Desage
"""

################################################################################
### 2. IMPORTS 																 ###
################################################################################

# GENERAL
import streamlit as st
import os


# STATIONS
from stations import accueil as station_accueil
from stations import ais as station_ais
from stations import meteo as station_meteo
from stations import message_op as station_message_op
from stations import journal_de_bord as j_de_b


@st.cache(allow_output_mutation=True)
def initialize_data():
    return {}


class NotAvailable():

    def write(self, *args, **kwargs):
        st.info("Cette ressource n'est pas encore disponible.")


################################################################################
### 3. MAIN CODE                                                             ###
################################################################################

# Stations dictionary
STATIONS = {
    #"Accueil": station_accueil,
    #"Admin": NotAvailable(),
    "Meteo": station_meteo,
    #"Opérations": NotAvailable(),
    #"Visualisations": NotAvailable()
    "Messages Opérationels": station_message_op,
    "AIS": station_ais,
    "Journal de Bord": j_de_b
}

#------------------------------------#
#- MAIN STREAMLIT LAUNCHER FUNCTION -#
#------------------------------------#


def main():
    """Main function of the App"""
    st.sidebar.title("Programme ESC")

    selection = st.sidebar.radio("Aller à", list(STATIONS.keys()))

    # # Authentification
    # try:
    #     authentified
    # except:
    #     authentified = {'auth': False}

    # if not authentified['auth']:
    #     block1 = st.empty()
    #     password = block1.text_input("Mot de Passe", value="")

    # if password == 'EcoNature2021':
    #     authentified['auth'] = True
    #     block1.empty()
    # elif password == '':
    #     pass
    # else:
    #     st.error('Mot de passe incorrect !')

    # # Important authentified code
    # if authentified['auth']:
    page = STATIONS[selection]

    data_dict = initialize_data()

    with st.spinner(f"Chargement ..."):
        page.write(data_dict=data_dict)

    st.sidebar.title("Important")
    # st.sidebar.info(
    #     "[Site Web](https://github.com/YsaelDesage/OverOneThousand)\n\n"
    #     "[Répertoire GitHub](https://github.com/YsaelDesage/OverOneThousand)"
    # )
    #st.sidebar.info(
    #    "Ceci est une version préliminaire d'essai. Toute utilisation commerciale ou redistribution est stricement interdite. \n\n Merci de transmettre vos questions et commentaires à ysael.desage@me.com ou à pscalabrini@hotmail.ca."
    #)
    st.sidebar.title("Auteurs")
    st.sidebar.info(
        "Ysael Desage"
    )
    #-------------------#
    #- END OF FUNCTION -#
    #-------------------#

################################################################################
### 4. MAIN EXECUTION CODE                                                   ###
################################################################################


if __name__ == "__main__":

    st.set_page_config()
    main()

################################################################################
### X. END OF CODE                                                           ###
################################################################################
