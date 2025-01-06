from collections import defaultdict
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

# +-------------------------+
# | Predicted Score Methods |
# +-------------------------+

def predict_score_method1(G, source, target, k=3): # k is the max paths to consider
    paths = list(nx.all_simple_paths(G, source=source, target=target, cutoff=k)) # default is dijkstra
    
    scores = []
    for path in paths:
        path_score = sum(G[path[i]][path[i+1]]['weight'] for i in range(len(path) - 1))

        decay_factor = 1 / ((len(path) - 1) ** 2)  # or np.exp(-len(path))
        scores.append(path_score * decay_factor)

        # dividing by (len(path) - 1) once gives the mean
        # dividing by (len(path) - 1) twice gives the weight

        if len(path) > 3:
            factored_score = (1 / (len(path) - 1) ** function_order) * (path_score ** function_order)
        else:
            factored_score = path_score / (len(path) - 1)

        scores.append(factored_score)

    return np.mean(scores)

function_order = 5 # cubic

def predict_score_method2(G, source, target, k=3): # k is the max paths to consider
    paths = list(nx.all_simple_paths(G, source=source, target=target, cutoff=k)) # default is dijkstra
    
    scores = []

    for path in paths:
        path_score = sum(G[path[i]][path[i+1]]['weight'] for i in range(len(path) - 1))

        if len(path) > 2:
            factored_score = (1 / (len(path) - 1) ** function_order) * (path_score ** function_order)
        else: # path is at least two
            factored_score = path_score / (len(path) - 1)

        scores.append(factored_score)

    return np.mean(scores)

# No weights on the length of the path
def predict_score_method3(G, source, target, k=3): # k is the max paths to consider
    paths = list(nx.all_simple_paths(G, source=source, target=target, cutoff=k)) # default is dijkstra
    
    scores = []
    for path in paths:
        path_score = sum(G[path[i]][path[i+1]]['weight'] for i in range(len(path) - 1))
        scores.append(path_score / (len(path) - 1))

    return np.mean(scores)

# Uses a simple weighted mean (of the additive inverses of the values)
def predict_score_method4(G, source, target, k=3): # k is the max paths to consider
    paths = list(nx.all_simple_paths(G, source=source, target=target, cutoff=k)) # default is dijkstra
    
    scores = defaultdict(list)
    for path in paths:
        path_score = sum(G[path[i]][path[i+1]]['weight'] for i in range(len(path) - 1))
        scores[len(path) - 1].append(path_score / (len(path) - 1))

    path_length_keys = list(scores.keys())

    final_score = 0
    for path_length, score_list in scores.items():
        factor = (max(path_length_keys) + min(path_length_keys) - path_length) / sum(path_length_keys)
        final_score += factor * np.mean(score_list)
        # scores[path_length] = np.mean(score_list)

    return final_score


unfinished_matches_copy = unfinished_matches.copy()
unfinished_matches_copy['predicted_score_method1'] = unfinished_matches_copy.apply(
    lambda row: predict_score_method1(G, source=row['home_team'], target=row['away_team'], k=3), axis=1)
unfinished_matches_copy['predicted_score_method2'] = unfinished_matches_copy.apply(
    lambda row: predict_score_method2(G, source=row['home_team'], target=row['away_team'], k=3), axis=1)
unfinished_matches_copy['predicted_score_method3'] = unfinished_matches_copy.apply(
    lambda row: predict_score_method3(G, source=row['home_team'], target=row['away_team'], k=3), axis=1)
unfinished_matches_copy['predicted_score_method4'] = unfinished_matches_copy.apply(
    lambda row: predict_score_method4(G, source=row['home_team'], target=row['away_team'], k=3), axis=1)

columns_to_normalize = ['predicted_score_method1', 'predicted_score_method2', 'predicted_score_method3', 'predicted_score_method4']
for column in columns_to_normalize:
    unfinished_matches_copy[column] = (unfinished_matches_copy[column] - unfinished_matches_copy[column].min()) / (unfinished_matches_copy[column].max() - unfinished_matches_copy[column].min())

unfinished_matches_copy['name'] = unfinished_matches_copy['home_team'] + ' vs ' + unfinished_matches_copy['away_team']
unfinished_matches_copy['name'] = unfinished_matches_copy['name'] + ' (' + unfinished_matches_copy['date'].apply(lambda x: x[5:10]) + ')'

print(unfinished_matches_copy.sort_values(by='predicted_score_method4', ascending=True, key=abs).head(10))

# +---------------------------+
# | Plotting Predicted Scores |
# +---------------------------+

plt.figure(figsize=(12, 9))

sorted_unfinished_matches = unfinished_matches_copy.sort_values(by='predicted_score_method4', ascending=True, key=abs)

plt.plot(sorted_unfinished_matches['name'], abs(sorted_unfinished_matches['predicted_score_method1']), label='predicted_score_method1')
plt.plot(sorted_unfinished_matches['name'], abs(sorted_unfinished_matches['predicted_score_method2']), label='predicted_score_method2')
plt.plot(sorted_unfinished_matches['name'], abs(sorted_unfinished_matches['predicted_score_method3']), label='predicted_score_method3')
plt.plot(sorted_unfinished_matches['name'], abs(sorted_unfinished_matches['predicted_score_method4']), label='predicted_score_method4')

plt.xticks(rotation=90)
plt.legend()
plt.show()
