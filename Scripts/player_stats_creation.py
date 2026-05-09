import pandas as pd
deliveries=pd.read_csv("deliveries.csv")
matches=pd.read_csv("matches.csv")

deliveries=deliveries.merge(
    matches[['id','season']],
    left_on='match_id',
    right_on='id',
    how='left'
)

print(deliveries.columns)

batting_stats=deliveries.groupby(['batter','season']).agg({
    'batsman_runs':'sum',
    'ball':'count',
    'match_id':'nunique'
}).reset_index()

batting_stats.rename(columns={
    'batsman_runs':'runs',
    'batter':'player_name',
    'match_id':'matches',
    'ball':'balls',
    'season':'year'
},inplace=True)

batting_stats['strike_rate']=(
    batting_stats['runs']/
    batting_stats['balls']
)*100

bowling_stats=deliveries.groupby(['bowler','season']).agg({
    'player_dismissed':'count',
    'total_runs':'sum',
    'ball':'count'
}).reset_index()

bowling_stats.rename(columns={
    'player_dismissed':'wickets',
    'bowler':'player_name',
    'total_runs':'run_conceded',
    'ball':'balls_bowled',
    'season':'year'
},inplace=True)

bowling_stats['overs']=bowling_stats['balls_bowled']/6

bowling_stats['economy']=(
    bowling_stats['run_conceded']/
    bowling_stats['overs']
)

player_stats=pd.merge(
    batting_stats,
    bowling_stats,
    on=['player_name','year'],
    how='outer'
)

player_stats.fillna(0,inplace=True)

player_stats.to_csv(
    'data/player_stats.csv',
    index=False
)

print("player stats created successfully")