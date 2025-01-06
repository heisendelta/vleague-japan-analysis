from collections import defaultdict
import networkx as nx
import numpy as np
import pandas as pd

# ensure the scores are inputted from the alphabetically lower team to the larger team
all_scores = defaultdict(lambda: [])
finished_matches = pd.read_csv('data/finished_matches.csv')
unfinished_matches = pd.read_csv('data/unfinished_matches.csv')

for i, row in finished_matches.iterrows():
    winning_team = row['winning_team']
    losing_team = row['losing_team']
    losing_score = int(row['score'].split('-')[-1])
    matchup_score = (3 - losing_score) / 3 # max number of matches is 3

    if winning_team > losing_team: 
        matchup_score *= -1 # score are stored from alphabetically lesser to greater team

    all_scores[frozenset([winning_team, losing_team])].append(matchup_score)


G = nx.DiGraph()

for teams, scores in all_scores.items():
    teamA, teamB = map(lambda x: x, list(set(teams)))
    G.add_edge(teamA, teamB, weight=np.mean(scores))
    G.add_edge(teamB, teamA, weight=-np.mean(scores))

    print(np.mean(scores))

shortest_paths = nx.floyd_warshall_numpy(G, weight="weight")
teams = list(G.nodes)

unfinished_matches_copy = unfinished_matches.copy()
unfinished_matches_copy['predicted_score'] = unfinished_matches_copy.apply(
    lambda row: shortest_paths[teams.index(row['home_team'])][teams.index(row['away_team'])], axis=1)

unfinished_matches_copy.sort_values(by='predicted_score', ascending=False)
