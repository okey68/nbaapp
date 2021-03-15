from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leagueleaders
from nba_api.stats.endpoints import playerdashboardbygamesplits
import pandas as pd
import time
import numpy as np




def get_nba_id():
        nba_players = players.get_active_players()
        
        playerdf = pd.DataFrame()
        
        for player in nba_players:
            career_stats = playercareerstats.PlayerCareerStats(player_id=player['id'])
            career_df = career_stats.get_data_frames()[0]
            career_df['NAME'] = player['full_name']

            grouped = career_df.groupby(["PLAYER_ID"]).sum(numeric_only=True)
            playerdf = pd.concat([playerdf,grouped], sort=False)
            
            time.sleep(.600)
            
        print(playerdf)
        playerdf.to_csv("NBA_PLAYERS_CAREER_STATS.csv")    

#get_nba_id()

##Getting dictionaries of all active NBA Players
nba_players = players.get_active_players()
player_dict = [players for players in nba_players if players['full_name'] == 'James Harden'][0]
#print('Number of players: {}'.format(len(nba_players)))
#print(player_dict)

##Putting the dictionaries into a data frame
data = nba_players
activePlayers_df = pd.DataFrame(data)
#print(activePlayers_df)


##Player names join with player stats dataframe
player_bio = pd.DataFrame(nba_players)
main_df = pd.read_csv("NBA_PLAYERS_CAREER_STATS.csv")

joined = pd.merge(main_df, player_bio, left_on=['PLAYER_ID'], right_on=['id'])

df = joined[['full_name', 'GP', 'GS', 'MIN', 'FGM', 'FGA',
       'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB',
       'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']].copy()
#print(df)


def league_leaders():
    leaders = leagueleaders.LeagueLeaders()
    leaders_df = leaders.get_data_frames()[0]   
    ranking_df = leaders_df[['PLAYER', 'RANK']]

    #LeagueLeader rank added to df
    ll_joined = pd.merge(df, ranking_df, left_on= ['full_name'], right_on= ['PLAYER'])
    ll_joined.to_csv('NBARANK.csv')
league_leaders()
df = pd.read_csv('NBARANK.csv')

#ranking_system
df['pts_rnk'] = df['PTS'].rank(ascending = False, method = 'min')
df['blk_rnk'] = df['BLK'].rank(ascending = False, method = 'min')
df['stl_rnk'] = df['STL'].rank(ascending = False, method = 'min')
df['ast_rnk'] = df['AST'].rank(ascending = False, method = 'min')
df['reb_rnk'] = df['REB'].rank(ascending = False, method = 'min')
df['oreb_rnk'] = df['OREB'].rank(ascending = False, method = 'min')  
df['fg_pct_rank'] = df['FG_PCT'].rank(ascending = False, method = 'min')
df['fg3_pct_rank'] = df['FG3_PCT'].rank(ascending = False, method = 'min')
df['ft_pct_rnk'] = df['FT_PCT'].rank(ascending = False, method = 'min')

ptsWeight = .80
rankWeight = .40
blkWeight = .05
stlWeight = .15
astWeight = .40
rebWeight = .50
orebWeight = .10
fgWeight = .13
fg3Weight = .10
ftWeight = .04

ranking = ((df['pts_rnk'] * ptsWeight)
            + (df['blk_rnk'] * blkWeight) 
            + (df['stl_rnk'] * stlWeight) 
            + (df['ast_rnk'] * astWeight) 
            + (df['reb_rnk'] * rebWeight) 
            + (df['oreb_rnk'] * orebWeight) 
            + (df['fg_pct_rank'] * fgWeight)
            + (df['fg3_pct_rank'] * fg3Weight)
            + (df['ft_pct_rnk'] * ftWeight)
            + (df['RANK'] * rankWeight)
            )
df['Total_Rank'] = ranking
df = df.sort_values(by='Total_Rank', ascending = True)

del df['PLAYER']
del df['Unnamed: 0']

df = df[['full_name', 'PTS', 'AST', 'REB', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'STL', 'BLK']]


print(df)
df.to_csv('NBARANK.csv')