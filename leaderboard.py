from collections import defaultdict
import numpy as np
import pandas as pd

finished_matches = pd.read_csv('data/finished_matches.csv')
unfinished_matches = pd.read_csv('data/unfinished_matches.csv')

# To evaluate the metrics, let's compare the predicted scores with the differences in leaderboard positions
set_leaderboard_wins = defaultdict(int)
set_leaderboard_losses = defaultdict(int)
match_leaderboard_wins = defaultdict(int)
match_leaderboard_losses = defaultdict(int)

leaderboard = pd.DataFrame(0, columns=['sets_won', 'sets_lost', 'matches_won', 'matches_lost'], 
                           index=list(set(finished_matches['winning_team']).union(set(finished_matches['losing_team']))))

for _, row in finished_matches.iterrows():
    winning_team = row['winning_team']
    losing_team = row['losing_team']

    winning_sets = 3
    losing_sets = int(row['score'].split('-')[-1])

    leaderboard.loc[winning_team, 'sets_won'] += winning_sets
    leaderboard.loc[losing_team, 'sets_won'] += losing_sets
    leaderboard.loc[winning_team, 'sets_lost'] += losing_sets
    leaderboard.loc[losing_team, 'sets_lost'] += winning_sets

    leaderboard.loc[winning_team, 'matches_won'] += 1
    leaderboard.loc[losing_team, 'matches_lost'] += 1

leaderboard['set_win_ratio'] = leaderboard['sets_won'] / (leaderboard['sets_won'] + leaderboard['sets_lost'])
leaderboard['match_win_ratio'] = leaderboard['matches_won'] / (leaderboard['matches_won'] + leaderboard['matches_lost'])

leaderboard['mean_win_ratio'] = (leaderboard['set_win_ratio'] + leaderboard['match_win_ratio']) / 2

print(leaderboard.sort_values(by='mean_win_ratio', ascending=False))
