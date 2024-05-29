
import json
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
with open('reviews.json', 'r') as file:
reviews = json.load(file)
with open('games.json', 'r') as file:
games = json.load(file)
return reviews, games

def create_utility_matrix(reviews):
df = pd.DataFrame(reviews)
utility_matrix = df.pivot_table(values='valutazione', index='id_utente', columns='id_gioco')
return utility_matrix

def calculate_similarity(utility_matrix):
similarity_matrix = cosine_similarity(utility_matrix.fillna(0))
return similarity_matrix

def recommend_games(user_id, utility_matrix, similarity_matrix):
try:
user_index = utility_matrix.index.get_loc(user_id)
similar_users = similarity_matrix[user_index]
similar_users_indices = similar_users.argsort()[::-1]
recommended_games = []

    for user_idx in similar_users_indices:
        if user_idx != user_index:
            recommended_games.extend(utility_matrix.iloc[user_idx].dropna().index.tolist())

    return list(set(recommended_games))[:10]
except KeyError:
    return []
if name == "main":
reviews, games = load_data()
utility_matrix = create_utility_matrix(reviews)
similarity_matrix = calculate_similarity(utility_matrix)

user_id = 1  # Id utente di esempio
recommendations = recommend_games(user_id, utility_matrix, similarity_matrix)

recommended_games = [game for game in games if game['id'] in recommendations]
with open('recommendations.json', 'w') as file:
    json.dump(recommended_games, file, indent=4)
