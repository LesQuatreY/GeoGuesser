import math
import streamlit as st

from map import Map
from utils import (
    get_list_communes, get_geoloc, get_distance, get_surface, rerun
    )
from streamlit_folium import st_folium

#Configuration de la page
st.set_page_config(
    page_title="GeoGuesser",
    layout="wide"
)
st.title("GeoGuesser")  

#Paramètres
HEIGHT=500
WIDTH=500

#Choix de l'utilisateur
nb_tour = int(st.sidebar.text_input("Nombre de tours ?", value=0))
if nb_tour==0: st.stop()

#Initialisation
if not "villes_a_placer" in st.session_state:
    st.session_state["villes_a_placer"] = get_list_communes(nb_tour=nb_tour)
if not "score" in st.session_state:
    st.session_state["score"] = 0
if not "tour" in st.session_state:
    st.session_state["tour"] = 0

#Lancement jeu
def quizz_for_one_city(ville):
    st.info("Placer la ville suivante : {}".format(ville))
    mapper=Map()
    if not "user_point" in st.session_state:
        map = st_folium(
            mapper.map(), returned_objects=["last_clicked"], height=HEIGHT, width=WIDTH
        )
        if not map["last_clicked"]: st.stop()
        else: st.session_state["user_point"] = list(map["last_clicked"].values())
        st.experimental_rerun()
    else:
        distance = get_distance(st.session_state["user_point"],get_geoloc(ville))    
        mapper.marker(st.session_state["user_point"], popup="Point placé", icon="https://www.iconpacks.net/icons/2/free-location-pin-icon-2965-thumb.png")
        mapper.marker(get_geoloc(ville),popup=ville,icon="https://www.iconpacks.net/icons/2/free-location-pin-icon-2965-thumb.png")
        mapper.line(st.session_state["user_point"],get_geoloc(ville))
        mapper.circle(get_geoloc(ville), rayon=distance)
        st_folium(mapper.map(), returned_objects=[""], height=HEIGHT, width=WIDTH)

    if distance<math.sqrt(get_surface(ville)/100)/2: score=0
    else: score=distance - math.sqrt(get_surface(ville)/100)/2

    distance = "{:.2f}km".format(distance) if distance>1 else "{:.0f}mètres".format(distance*1000)

    st.session_state["score"] += score 

    col1, col2 = st.columns(2)
    col1.metric("Erreur", distance)
    col2.metric("Score", round(st.session_state["score"],2))

if st.session_state["tour"]<nb_tour:
    tour = st.session_state["tour"]
    quizz_for_one_city(st.session_state["villes_a_placer"][tour])
    st.session_state["tour"] += 1
    del st.session_state["user_point"]
    st.button("Tour suivant")
else:
    st.metric("Score", round(st.session_state["score"],2))
    if st.button("Rejouer"): rerun()
