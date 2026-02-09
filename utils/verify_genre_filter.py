import pickle
import pandas as pd

try:
    movies = pickle.load(open('movies_df.pkl', 'rb'))
    
    genre_map = {
        "Action": "action",
        "Adventure": "adventur",
        "Animation": "anim",
        "Comedy": "comedi",
        "Crime": "crime",
        "Drama": "drama",
        "Fantasy": "fantasi",
        "Horror": "horror",
        "Romance": "romanc",
        "Science Fiction": "sciencefict",
        "Thriller": "thriller"
    }
    
    for genre, keyword in genre_map.items():
        count = movies[movies['tags'].apply(lambda x: keyword in x if isinstance(x, str) else False)].shape[0]
        print(f"{genre}: {count} movies found")
        
    keyword = "sciencefict"
    filtered_movies = movies[movies['tags'].apply(lambda x: keyword in x if isinstance(x, str) else False)].head(5)
    print("\nSample Science Fiction movies:")
    print(filtered_movies['title'].tolist())
    
except Exception as e:
    print(e)
