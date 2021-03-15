from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import pandas as pd
import streamlit as st 



def nbamultiapp():
    st.write("""
    # player career stats 
    ### type a player (accurately and completely)

    """)

    player_name = st.text_input("Player", 'Michael Jordan')

    nba_players = players.get_players()
    player_dict = [player for player in nba_players if player['full_name'] == player_name][0]
    #print(player_dict)

    career_stats = playercareerstats.PlayerCareerStats(player_id=player_dict['id'])
    playerdf = career_stats.get_data_frames()[0]
    df = pd.DataFrame(playerdf)
    df['Name'] = player_dict['full_name']
    df = df[['Name', 'SEASON_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'PTS', 'FG_PCT', 'FG3_PCT', 'REB', 'AST', 'BLK']]
    #print(df)
    st.table(df)
