import pickle
import pandas as pd

try:
    movies = pickle.load(open('movies_df.pkl', 'rb'))
    print("Columns:", movies.columns.tolist())
    
    if 'genres' in movies.columns:
        print("Format of genres (first 5):")
        print(movies['genres'].head())
        # Check if genres are lists or strings
        first_val = movies['genres'].iloc[0]
        print(f"Type of genre data: {type(first_val)}")
    else:
        print("'genres' column missing!")
        
except Exception as e:
    print(e)
