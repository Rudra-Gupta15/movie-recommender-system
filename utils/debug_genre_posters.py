import pickle
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        
        # Create a session with retry logic
        session = requests.Session()
        retry = requests.adapters.Retry(total=3, backoff_factor=0.5)
        adapter = requests.adapters.HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        response = session.get(url, timeout=10)

        # If API request fails
        if response.status_code != 200:
            print(f"Failed to fetch {movie_id}: {response.status_code}")
            return None

        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            print(f"No poster path for {movie_id}")
            return None

    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return None

try:
    movies = pickle.load(open('movies_df.pkl', 'rb'))
    
    # Check for specific movies mentioned by user
    targets = ["Robin Hood", "The Lovers"]
    
    for title in targets:
        matches = movies[movies['title'] == title]
        if not matches.empty:
            movie_id = matches.iloc[0].movie_id
            print(f"\nChecking {title} (ID: {movie_id})...")
            poster = fetch_poster(movie_id)
            print(f"Poster URL: {poster}")
        else:
            print(f"\nMovie '{title}' not found in dataset")
            
except Exception as e:
    print(e)
