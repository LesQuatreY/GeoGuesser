import requests

import api_access

def get_list_communes(top=100, nb_tour=20):
    import random
    return random.sample(
        list(map(lambda x: x["nom"], sorted(requests.get(
        "https://geo.api.gouv.fr/communes?fields=nom,population&zone=metro&geometry=centre&boost=population"
        ).json(), key= lambda d: d["population"], reverse=True
        )[0:top])), nb_tour
    )

def get_surface(ville):
    return requests.get(
        f"https://geo.api.gouv.fr/communes?nom={ville}&fields=nom,surface&zone=metro&geometry=centre&boost=population"
    ).json()[0]["surface"]

def get_geoloc(ville):
    return list(requests.get(
    "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format(
        ville,
        api_access.google_api_key
        )
    ).json()["results"][0]["geometry"]["location"].values())

def convertRad(input): #Conversion des degrés en radian
    import math
    return (math.pi*input)/180

def get_distance(point_a, point_b): #distance en km entre deux coordonnées gps
    import math
    lat_a,lon_a = convertRad(point_a[0]),convertRad(point_a[1])
    lat_b,lon_b = convertRad(point_b[0]),convertRad(point_b[1])
    return 6378*(math.pi/2 - math.asin( math.sin(lat_b) * math.sin(lat_a) + math.cos(lon_b - lon_a) * math.cos(lat_b) * math.cos(lat_a)))

def get_city(lat, lon):
    return requests.get(
        "https://api-adresse.data.gouv.fr/reverse/?lon={}&lat={}".format(lon,lat)
    ).json()["features"][0]["properties"]["city"]

def rerun():
    import streamlit as st
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()

