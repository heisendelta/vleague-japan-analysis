import pandas as pd
import numpy as np
from datetime import datetime

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

from venue_analysis import load_data
match_with_venues = load_data()


match_with_venues_copy = match_with_venues.copy()

match_with_venues_copy['date_numeric'] = (pd.to_datetime(match_with_venues_copy['date']) - pd.to_datetime(match_with_venues_copy['date']).min())
match_with_venues_copy['date_numeric'] = match_with_venues_copy['date_numeric'].dt.total_seconds() / (60 * 60 * 24)

features = match_with_venues_copy[['latitude', 'longitude', 'date_numeric']]

scaler = StandardScaler()
normalized_features = scaler.fit_transform(features)

db = DBSCAN(eps=0.5, min_samples=2, metric='euclidean')
match_with_venues_copy['cluster'] = db.fit_predict(normalized_features)

clustered_matches = match_with_venues_copy.groupby('cluster')
for cluster, matches in clustered_matches:
    if len(matches) > 2:
        if cluster == -1:
            print("\nOutliers:")
        else:
            print(f"\nCluster {cluster}:")

        match_info = matches[['date', 'home_team', 'away_team', 'venue', 'score']]
        print(match_info) # looks better in the ipynb notebook
        # print(matches[['date', 'home_team', 'away_team', 'venue']])

# Distance clustering is the same
# Time clustering: All dates in a cluster are required to be in a one-week time frame

match_with_venues_copy['date_numeric'] = pd.to_datetime(match_with_venues_copy['date'])
geo_features = match_with_venues_copy[['latitude', 'longitude']]

scaler = StandardScaler()
normalized_geo_features = scaler.fit_transform(geo_features)

geo_db = DBSCAN(eps=0.5, min_samples=2, metric='euclidean')
match_with_venues_copy['geo_cluster'] = geo_db.fit_predict(normalized_geo_features)

final_clusters = []
for cluster_id in match_with_venues_copy['geo_cluster'].unique():
    if cluster_id == -1:
        continue

    cluster_matches = match_with_venues_copy[match_with_venues_copy['geo_cluster'] == cluster_id]
    cluster_matches = cluster_matches.sort_values(by='date_numeric')

    current_cluster = []
    start_date = None
    for _, row in cluster_matches.iterrows():
        if not start_date:
            start_date = row['date_numeric']
            current_cluster.append(row)
        elif (row['date_numeric'] - start_date).days <= 7:
            current_cluster.append(row)
        else:
            final_clusters.append(current_cluster)
            current_cluster = [row]
            start_date = row['date_numeric']

    if current_cluster:
        final_clusters.append(current_cluster)

clustered_matches = []
for cluster_id, matches in enumerate(final_clusters):
    for match in matches:
        match['final_cluster'] = cluster_id
        clustered_matches.append(match)

clustered_match_with_venues_copy = pd.DataFrame(clustered_matches)

for cluster, matches in clustered_match_with_venues_copy.groupby('final_cluster'):
    if len(matches) > 2:
        print(f"\nCluster {cluster}:")
        match_info = matches[['date', 'home_team', 'away_team', 'venue', 'score']]
        print(match_info.to_html())
