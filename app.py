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
    st.session_state.dark_mode = True

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
    toggle_color = "#ffffff" # White in Dark Mode
else:
    bg_color = "#eeeeee" # Light Grey
    text_color = "#121212" # Almost Black for best contrast
    navbar_bg = "#e0e0e0" # Slightly darker grey for sidebar/nav
    card_bg = "#ffffff"
    input_bg = "#ffffff"
    input_text = "#121212"
    secondary_text = "#444444"
    border_color = "#cccccc"
    toggle_color = "#000000" # Black in Light Mode

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

/* Sidebar Styling */
[data-testid="stSidebar"] {{
    background-color: {navbar_bg};
    border-right: 1px solid {border_color};
}}

[data-testid="stSidebar"] .stMarkdown {{
    color: {text_color};
}}

/* Headers */
h1, h2, h3, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {{
    font-family: 'Inter', sans-serif;
    color: {text_color} !important;
    font-weight: 700;
}}

/* Navbar Container */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: {navbar_bg}EE; /* Higher opacity for better visibility */
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 10px 40px; /* Adjusted padding */
    border-bottom: 
    1px solid {border_color};
    margin: -60px -5rem 30px -5rem;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
}}

/* Dropdown styling */
div[data-baseweb="select"] > div {{
    background-color: {input_bg};
    border: 1px solid {border_color};
    border-radius: 8px;
    color: {input_text};
}}

/* Dropdown Menu (Popover) Styling */
div[data-baseweb="popover"] ul {{
    background-color: {input_bg} !important;
    border: 1px solid {border_color} !important;
}}

div[data-baseweb="popover"] li {{
    color: {input_text} !important;
    background-color: transparent !important;
    transition: background 0.2s ease;
}}

div[data-baseweb="popover"] li:hover {{
    background-color: {navbar_bg} !important;
}}

/* Button Styling (Pill Shape) */
.stButton > button {{
    background-color: {input_bg};
    color: {text_color} !important;
    border: 1px solid {border_color};
    border-radius: 20px;
    padding: 0.6rem 2rem;
    font-weight: 700;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    white-space: nowrap !important; /* Prevent text wrapping */
    width: auto !important;
    min-width: fit-content !important;
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

/* Customize Selectbox/Toggle Labels */
label, .st-ck, .st-bj, [data-testid="stWidgetLabel"] p {{
    color: {text_color} !important;
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
    font-size: 2.2rem;
    font-weight: 900;
    margin-left: 20px;
    letter-spacing: -1.5px;
    background: linear-gradient(
        135deg, 
        {text_color} 0%, 
        #007bff 30%, 
        #00c6ff 50%, 
        #007bff 70%, 
        {text_color} 100%
    );
    background-size: 200% auto;
    color: {text_color};
    background-clip: text;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 5s ease-in-out infinite;
    display: inline-block;
    text-shadow: 0 10px 20px rgba(0, 123, 255, 0.2);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}}

.navbar-title:hover {{
    transform: scale(1.02);
    letter-spacing: -0.5px;
    text-shadow: 0 15px 30px rgba(0, 123, 255, 0.4);
}}

.title-emoji {{
    font-size: 2.4rem;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
    display: inline-block;
    transition: transform 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}}

.navbar-title:hover + .title-emoji, 
div:hover > .title-emoji {{
    transform: rotate(15deg) scale(1.2);
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
    background-color: {card_bg}; /* Solid background for cards */
    border: 1px solid {border_color};
    border-radius: 16px;
    padding: 15px;
    overflow: hidden;
    animation: fadeInUp 0.8s ease-out backwards;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}}

.movie-card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.15);
    border-color: #007bff;
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

/* UNIVERSAL EXTREME TOGGLE OVERRIDE - DESCENDANT TARGETING */
div[data-testid="stSidebar"] .stToggle div[data-testid="stCheckbox"] > div {{
    height: 50px !important;
    width: 100px !important;
    min-width: 100px !important;
    min-height: 50px !important;
    border: 3px solid {border_color} !important;
    background-color: {input_bg} !important;
    box-shadow: inset 0 4px 10px rgba(0,0,0,0.4) !important;
    border-radius: 25px !important;
    transition: all 0.3s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0 auto !important;
}}

/* The Knob - Targeted via Descendant */
div[data-testid="stSidebar"] .stToggle div[data-testid="stCheckbox"] > div > div {{
    height: 42px !important;
    width: 42px !important;
    min-width: 42px !important;
    min-height: 42px !important;
    background: linear-gradient(145deg, #ffffff, #d9d9d9) !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.5) !important;
    border-radius: 50% !important;
    left: 4px !important;
    top: 1px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}}

/* Active State (ON) */
div[data-testid="stSidebar"] .stToggle div[data-testid="stCheckbox"] div[data-checked="true"] {{
    background-color: {toggle_color} !important;
    border-color: {toggle_color} !important;
}}

div[data-testid="stSidebar"] .stToggle div[data-testid="stCheckbox"] div[data-checked="true"] > div {{
    left: calc(100% - 46px) !important;
    background: #007bff !important; /* Standout Blue when ON */
}}

/* Visibility when OFF */
div[data-testid="stSidebar"] .stToggle div[data-testid="stCheckbox"] div[data-checked="false"] {{
    border-color: {text_color} !important; /* Visible border in light mode */
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

# Sidebar Logic - RELOCATED & PERSISTENT
if 'show_settings' not in st.session_state:
    st.session_state.show_settings = False

with st.sidebar:
    st.header("🌗 Appearance")
    # Centers the toggle and icons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown('<div style="text-align: right; font-size: 1.2rem; margin-top: 5px;">☀️</div>', unsafe_allow_html=True)
    with col2:
        dark_mode_val = st.toggle(" ", value=st.session_state.dark_mode, label_visibility="collapsed")
        if dark_mode_val != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode_val
            st.rerun()
    with col3:
        st.markdown('<div style="text-align: left; font-size: 1.2rem; margin-top: 5px;">🌙</div>', unsafe_allow_html=True)
    
    st.divider()
    
    if st.session_state.show_settings:
        st.header("⚙️ Settings")
        st.checkbox("Show Ratings (Coming Soon)", value=False, disabled=True)
        st.write("More settings coming soon!")

# Top Navigation Bar Layout
col1, col2, col3 = st.columns([5, 2, 1])

with col1:
    # Read logo
    try:
        with open("logo.jpg", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; cursor: default;">
                <a href="https://rudra-portfolio-liart.vercel.app/" target="_blank">
                    <img src="data:image/jpeg;base64,{data}" class="logo-img">
                </a>
                <div style="display: flex; align-items: center; margin-left: 10px;">
                    <span class="title-emoji">🎬</span>
                    <span class="navbar-title">Movie Recommender System</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.markdown(
            """
            <div style="display: flex; align-items: center; cursor: default;">
                <img src="https://cdn-icons-png.flaticon.com/512/2503/2503508.png" class="logo-img">
                <div style="display: flex; align-items: center; margin-left: 10px;">
                    <span class="title-emoji">🎬</span>
                    <span class="navbar-title">Movie Recommender System</span>
                </div>
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
        st.session_state.show_settings = not st.session_state.show_settings
        st.rerun()


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
                        
                        poster_html = f'<img src="{poster}" style="width:100%; border-radius:12px;">' if poster else f'<div style="height:350px; background:{navbar_bg}; border-radius:12px; display:flex; flex-direction:column; align-items:center; justify-content:center; border: 1px dashed {border_color}; color:{secondary_text};"><span>🎬</span><br>No Poster Available</div>'
                        
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
                
                poster_html = f'<img src="{poster}" style="width:100%; border-radius:12px;">' if poster else f'<div style="height:350px; background:{navbar_bg}; border-radius:12px; display:flex; flex-direction:column; align-items:center; justify-content:center; border: 1px dashed {border_color}; color:{secondary_text};"><span>🎬</span><br>No Poster Available</div>'

                st.markdown(
                    f"""
                    <div class="movie-card" style="animation-delay: {delay}s;">
                        <div class="movie-title">{name}</div>
                        {poster_html}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


