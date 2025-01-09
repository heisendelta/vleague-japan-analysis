import pandas as pd
import numpy as np
from datetime import datetime


unfinished_matches = pd.read_csv('data/unfinished_matches_with_scores.csv')
unfinished_matches['mean_score'] = unfinished_matches[[
    c for c in unfinished_matches.columns if c.startswith('predicted_score')]].mean(axis=1)
unfinished_matches['score'] = 1 / unfinished_matches['mean_score']
unfinished_matches = unfinished_matches[['date', 'home_team', 'away_team', 'venue', 'score']]

venues = pd.read_csv('data/venues.csv').replace('-', pd.NA).dropna()
venues['time'] = venues['time'].apply(lambda x: datetime.strptime(x, '%Hh%Mm').time())

match_with_venues = unfinished_matches.merge(venues, on='venue', how='left').dropna(axis=0)
match_with_venues['date'] = match_with_venues['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M'))
match_with_venues['cost'] = match_with_venues['cost'].apply(int)


a = 1 # arbitrary constant for scaling

match_with_venues_copy = match_with_venues.copy()
match_with_venues_copy['score_per_cost'] = (a * abs(match_with_venues_copy['score'])) / match_with_venues_copy['cost']

match_with_venues_copy = match_with_venues_copy.sort_values(by='score_per_cost', ascending=False)
# match_with_venues_copy.drop(['time', 'latitude', 'longitude'], axis=1).head(20) # shows matches between the same teams consecutively
match_without_duplicates = match_with_venues_copy.loc[
    match_with_venues_copy[['home_team', 'away_team']].drop_duplicates(keep='first', inplace=False).index]
