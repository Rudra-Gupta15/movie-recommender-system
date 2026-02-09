# Import required libraries
import streamlit as st
import pickle
import pandas as pd
import requests
import os
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Get API key
API_KEY = os.getenv("API_KEY")

# Stop app if API key not found
if not API_KEY:
    st.error("API_KEY not found. Please check your .env file.")
    st.stop()

# ---------------- UI ---------------- #

st.set_page_config(page_title="Movie Recommender System", page_icon="🎬", layout="wide")


# Initialize Dark Mode State
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Define Colors based on Mode
if st.session_state.dark_mode:
    bg_color = "#333333"
    text_color = "#ffffff"
    navbar_bg = "#444444"
    card_bg = "#444444"
    input_bg = "#555555"
    input_text = "#ffffff"
    secondary_text = "#cccccc"
    border_color = "#555555"
else:
    bg_color = "#ffffff"
    text_color = "#333333"
    navbar_bg = "#ffffff"
    card_bg = "#ffffff"
    input_bg = "#f8f9fa"
    input_text = "#333333"
    secondary_text = "#555555"
    border_color = "#e0e0e0"

# Custom CSS for Theme
st.markdown(f"""
<style>
/* Import Google Fonts - Inter */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

/* General Styling */
.stApp {{
    background-color: {bg_color};
    font-family: 'Inter', sans-serif;
    color: {text_color};
}}

/* Headers */
h1, h2, h3 {{
    font-family: 'Inter', sans-serif;
    color: {text_color};
    font-weight: 700;
}}

/* Navbar Container */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: {navbar_bg};
    padding: 10px 20px;
    border-bottom: 1px solid {border_color};
    margin-bottom: 20px;
}}

/* Dropdown styling */
div[data-baseweb="select"] > div {{
    background-color: {input_bg};
    border: 1px solid {border_color};
    border-radius: 8px;
    color: {input_text};
}}

/* Button Styling (Pill Shape) */
.stButton > button {{
    background-color: {navbar_bg};
    color: {text_color};
    border: 1px solid {border_color};
    border-radius: 20px;
    padding: 0.5rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}}

.stButton > button:hover {{
    background-color: {input_bg};
    border-color: #cccccc;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transform: translateY(-1px);
}}

/* Image/Poster Styling */
img {{
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08); /* Subtle shadow for depth */
    transition: transform 0.3s ease;
}}

img:hover {{
    transform: scale(1.02); /* Slight lift on hover */
}}

/* Text Styling under posters */
.stText {{
    font-size: 0.9rem;
    font-weight: 500;
    text-align: center;
    color: {secondary_text};
    margin-top: 8px;
}}

/* Customize Selectbox Label */
label {{
    color: {secondary_text} !important;
    font-weight: 600;
}}

/* Logo Styling */
.logo-img {{
    width: 60px;
    height: 60px;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}}

.logo-img:hover {{
    transform: scale(1.1) rotate(5deg);
}}

/* Animated Title Styling */
@keyframes shimmer {{
    0% {{ background-position: -1000px 0; }}
    100% {{ background-position: 1000px 0; }}
}}

.navbar-title {{
    font-size: 1.8rem;
    font-weight: 800;
    margin-left: 15px;
    background: linear-gradient(to right, {text_color} 0%, #007bff 50%, {text_color} 100%);
    background-size: 200% auto;
    color: {text_color};
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s linear infinite;
    display: inline-block;
}}

/* Movie Card Animation */
@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translate3d(0, 40px, 0);
    }}
    to {{
        opacity: 1;
        transform: translate3d(0, 0, 0);
    }}
}}

.movie-card {{
    background-color: transparent;
    border-radius: 12px;
    overflow: hidden;
    animation: fadeInUp 0.8s ease-out backwards;
}}

.movie-title {{
    font-size: 1rem;
    font-weight: 600;
    text-align: center;
    color: {text_color};
    margin-bottom: 5px;
    height: 3em;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}}

/* Settings Button */
.settings-btn {{
    font-size: 1.2rem;
    cursor: pointer;
    color: {secondary_text};
    transition: color 0.3s ease;
}}

.settings-btn:hover {{
    color: #007bff;
    transform: rotate(90deg);
}}
</style>
""", unsafe_allow_html=True)

# Load movie data
movies = pickle.load(open('movies_df.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))



# Function to fetch poster from TMDB

# Function to get a cached session
@st.cache_resource
def get_session():
    session = requests.Session()
    retry = requests.adapters.Retry(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Function to fetch movie poster
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        
        # Use cached session
        session = get_session()
        response = session.get(url, timeout=10)

        # If API request fails
        if response.status_code != 200:
            return None

        data = response.json()

        # Get poster path
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return None

    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return None




# Recommendation function
def recommend(movie):

    # Get index of selected movie
    movie_index = movies[movies['title'] == movie].index[0]

    # Get similarity scores
    distances = similarity[movie_index]

    # Get top 5 similar movies
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters




# ---------------- UI ---------------- #

# Custom CSS for Navbar and Logo

# Sidebar for Settings
if 'show_settings' not in st.session_state:
    st.session_state.show_settings = False

if st.session_state.show_settings:
    with st.sidebar:
        st.header("Settings")
        st.write("Configure your preferences here.")
        # Dark Mode Toggle
        st.toggle("Dark Mode", key="dark_mode")
        st.checkbox("Show Ratings (Coming Soon)", value=False, disabled=True)




# Top Navigation Bar Layout
col1, col2, col3 = st.columns([5, 2, 1])

with col1:
    # Read logo
    try:
        with open("logo.jpg", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(
            f"""
            <div style="display: flex; align-items: center;">
                <a href="https://rudra-portfolio-liart.vercel.app/" target="_blank">
                    <img src="data:image/jpeg;base64,{data}" class="logo-img">
                </a>
                <span class="navbar-title">🎬Movie Recommender System</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.markdown(
            """
            <div style="display: flex; align-items: center;">
                <img src="https://cdn-icons-png.flaticon.com/512/2503/2503508.png" class="logo-img">
                <span class="navbar-title">🎬Movie Recommender System</span>
            </div>
            """,
            unsafe_allow_html=True
        )

# Genre Mapping
genre_map = {
    "All": None,
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

with col2:
    selected_genre = st.selectbox("Genre", list(genre_map.keys()), label_visibility="collapsed")

with col3:
    if st.button("⚙️ Settings"):
        st.session_state.show_settings = not st.session_state.get('show_settings', False)



# Main Content Logic
if selected_genre != "All":
    st.subheader(f"Top 10 {selected_genre} Movies")
    
    # Filter movies by genre keyword
    keyword = genre_map[selected_genre]
    try:
        # Check if 'tags' column exists and filter
        if 'tags' in movies.columns:
            filtered_movies = movies[movies['tags'].apply(lambda x: keyword in x if isinstance(x, str) else False)]
        else:
            st.error("Data error: 'tags' column missing.")
            filtered_movies = pd.DataFrame()
            
        if not filtered_movies.empty:
            # Display top 10 (or fewer if less available)
            top_movies = filtered_movies.head(10)
            

            # Create a grid layout for results
            # Rows of 5 movies each
            for i in range(0, len(top_movies), 5):
                cols = st.columns(5)
                batch = top_movies.iloc[i:i+5]
                
                for idx, (col, (_, row)) in enumerate(zip(cols, batch.iterrows())):
                    with col:
                        poster = fetch_poster(row.movie_id)
                        # Staggered animation delay (0.2s * index in batch) + base delay for row
                        delay = (i // 5) * 1.0 + (idx * 0.2) 
                        
                        poster_html = f'<img src="{poster}" style="width:100%; border-radius:12px;">' if poster else '<div style="height:300px; background:#f0f0f0; border-radius:12px; display:flex; align-items:center; justify-content:center;">No Image</div>'
                        
                        st.markdown(
                            f"""
                            <div class="movie-card" style="animation-delay: {delay}s;">
                                <div class="movie-title">{row.title}</div>
                                {poster_html}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
        else:
            st.info(f"No movies found for genre: {selected_genre}")

    except Exception as e:
        st.error(f"Error filtering movies: {e}")

else:
    # Default Recommender View
    st.subheader("Discover Movies Like...")


    # Dropdown to select movie
    selected_movie = st.selectbox(
        "Select a movie",
        movies['title'].values
    )

    # Recommend button
    if st.button("Recommend"):

        names, posters = recommend(selected_movie)

        # Create columns
        cols = st.columns(5)

        for idx, (col, name, poster) in enumerate(zip(cols, names, posters)):
            with col:
                delay = idx * 0.2 # 0.2s staggered delay
                
                poster_html = f'<img src="{poster}" style="width:100%; border-radius:12px;">' if poster else '<div style="height:300px; background:#f0f0f0; border-radius:12px; display:flex; align-items:center; justify-content:center;">No Image</div>'

                st.markdown(
                    f"""
                    <div class="movie-card" style="animation-delay: {delay}s;">
                        <div class="movie-title">{name}</div>
                        {poster_html}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


