import playergamelogs
import nba_app
import careerstats
import streamlit as st
from PIL import Image

image = Image.open('new-kobe-nba-logo.png')
st.image(image, width=150)


PAGES = {
    "NBA Rankings": nba_app,
    "Game Logs": playergamelogs,
    "Career Stats": careerstats
}

st.sidebar.title('Pages')
selection = st.sidebar.radio("Go To:", list(PAGES.keys()))
page = PAGES[selection]
page.nbamultiapp()