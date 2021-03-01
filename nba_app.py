import pandas as pd
import streamlit as st
from nba_api.stats.static import players

def nbamultiapp():
    df = pd.read_csv("NBARANK.csv")
    del df['Unnamed: 0']
    st.title("nba player rankings")
    st.write("""
    ##### All current NBA players ranked by skill and acheivement based on career statistics
    """)
    st.write("""
    ###### Only active players
    """)

    st.table(df)


