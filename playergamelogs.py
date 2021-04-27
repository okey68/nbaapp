from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelogs
from nba_api.stats.library.parameters import SeasonAll 
import pandas as pd
import time
import streamlit as st

def nbamultiapp():
    st.write("""
    # player game log by year
    ### type a player, pick a year
    
    """)
    years = ['2020-21','2019-20','2018-19','2017-18','2016-17', '2015-16','2014-15','2013-14','2012-13']
    player_name = st.text_input("Player (name must be spelled correctly)", 'LeBron James')
    years_input = st.selectbox("Year", years)
    
    nba_players = players.get_players()
    player_dict = [player for player in nba_players if player['full_name'] == player_name][0]
    #print(player_dict)

    allGameLogs = playergamelogs.PlayerGameLogs(player_id_nullable=player_dict['id'], season_nullable= years_input)
    playerdf = allGameLogs.get_data_frames()[0]
    df = pd.DataFrame(playerdf)
    #print(df)
    df =  df[['SEASON_YEAR','PLAYER_NAME','TEAM_ABBREVIATION', 'GAME_DATE', 'MATCHUP','WL','PTS','REB','AST','STL','TOV']]
    st.table(df)


