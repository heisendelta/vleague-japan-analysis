import numpy as np
import pandas as pd

leaderboard = pd.read_csv('data/leaderboard.csv')

# USAGE: "unfinished_matches_copy" is a dataframe with all of the (home_team, away_team) combinations
# and the predicted scores as different columns starting with "predicted_score"

# TODO: Soft-code "predicted_score_method{i}" by iterating over all columns starting with "predicted_score"
# so that this works dynamically with more than 4 scores to test (4 is constant in the loops below)

# Uses least-squares to calculate error (squares each error and take the mean at the end)
def evaluate_predicted_scores(unfinished_matches_copy):
    def return_unique_team_combos(df):
        seen_combinations = set()

        unique_indices = []

        for idx, row in df.iterrows():
            team_combination = frozenset([row['home_team'], row['away_team']])
            
            if team_combination not in seen_combinations:
                seen_combinations.add(team_combination)
                unique_indices.append(idx)

        unique_matches = df.loc[unique_indices]

        unique_matches.reset_index(drop=True, inplace=True)
        return unique_matches

    unique_unfinished_matches = return_unique_team_combos(unfinished_matches_copy)

    metrics_dict = {f'predicted_score_method{i}': [] for i in range(1, 5)}

    for _, row in unique_unfinished_matches.iterrows():
        home_team = row['home_team']
        away_team = row['away_team']
        diff_mean_ratio = abs(leaderboard.loc[home_team, 'mean_win_ratio'] - leaderboard.loc[away_team, 'mean_win_ratio'])


        for i in range(1, 5):
            predicted_score = row[f'predicted_score_method{i}']
            error = np.sqrt((predicted_score - diff_mean_ratio) ** 2)
            metrics_dict[f'predicted_score_method{i}'].append(error)

    # Ends with a printn statement, modify for the values
    for i in range(1, 5):
        print(f'predicted_score_method{i}', np.mean(metrics_dict[f'predicted_score_method{i}']))
