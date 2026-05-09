import numpy as np
import pandas as pd

auction=pd.read_csv("IPLPlayerAuctionData.csv")
player_stats=pd.read_csv("player_stats.csv")

print(auction.columns)
print(player_stats.columns)

auction.rename(columns={
    'Player':'player_name',
    'Amount':'sold_price',
    'Team':'team',
    'Year':'year'
    },inplace=True)


print(auction['year'].head())
print(auction['year'].dtype)

print(player_stats['year'].head())
print(player_stats['year'].dtype)


auction['year'] = pd.to_numeric(
    auction['year'],
    errors='coerce'
)
auction = auction.dropna(subset=['year'])
auction['year'] = auction['year'].astype(int)


player_stats['year'] = player_stats['year'].astype(str)
player_stats['year'] = player_stats['year'].str.extract(r'(\d{4})')
player_stats['year'] = pd.to_numeric(
    player_stats['year'],
    errors='coerce'
)
player_stats = player_stats.dropna(subset=['year'])
player_stats['year'] = player_stats['year'].astype(int)

merged=pd.merge(
    auction,
    player_stats,
    on=['player_name','year'],
    how='left'
)

print(merged.head())

merged.fillna(0,inplace=True)

print(merged[['runs','strike_rate','wickets','matches','sold_price']].corr())

merged['value_score']=(
    merged['runs']*0.43+
    merged['strike_rate']*0.15+
    merged['wickets']*0.05+
    merged['matches']*0.37
)

merged['normalized_score']=(
    (merged['value_score']-merged['value_score'].min())/
    (merged['value_score'].max()-merged['value_score'].min())
)*100

merged['fair_price']=(
    merged['normalized_score']*
    merged['sold_price'].mean()
)

merged['difference']=(
    merged['sold_price']-
    merged['fair_price']
)

merged['status']=np.where(
    merged['difference']>0,
    'Overpaid',
    'Undervalued'
)

team_analysis=merged.groupby('team')['difference'].mean()

role_analysis=merged.groupby('Role')['fair_price'].mean()

merged.to_csv("final_auction_analysis.csv",index=False)

print("Final auction analysis created sucessfully!")