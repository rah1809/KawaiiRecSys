import streamlit as st
import pandas as pd
import sys
import os
import streamlit.components.v1 as components

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Import from our new modular structure
from src.hybrid import hybrid_recommend
from utils.helpers import (
    get_anime_image,
    genre_to_color,
    load_anime_data,
    get_random_quote
)

# Streamlit page setup
st.set_page_config(
    page_title="KawaiiRecSys",
    page_icon="🎌",
    layout="wide"
)

# Enhanced Netflix-style CSS
st.markdown("""
    <style>
        html, body {
            background-color: #0e0e10;
            color: white;
        }
        .block-container {
            padding-top: 2rem;
            background-color: #0e0e10;
        }
        h1, h2, h3 {
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 600;
        }
        .stButton button {
            background: linear-gradient(145deg, #ff4baf, #ff0055);
            color: white;
            border-radius: 10px;
            border: none;
            font-weight: bold;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
            font-size: 1.2em;
            width: 100%;
            margin-top: 1rem;
        }
        .stButton button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 15px rgba(255, 75, 175, 0.5);
        }
        .stSlider > div[data-baseweb="slider"] > div {
            background: linear-gradient(to right, #ff4baf, #ff0055);
        }
        .stNumberInput>div>div>input, .stTextInput>div>div>input {
            background-color: #1c1c1e;
            color: white;
            border-radius: 12px;
            border: 1px solid #ff4baf;
        }
        .quote-footer {
            margin-top: 3rem;
            color: #aaaaaa;
            font-style: italic;
            text-align: center;
            padding: 1rem;
            border-top: 1px solid rgba(255, 75, 175, 0.2);
        }
        .stMultiSelect > div {
            background-color: #1c1c1e;
            color: white;
            border-radius: 12px;
            border: 1px solid #ff4baf;
        }
        .stMultiSelect > div > div > div {
            color: white;
        }
        .recommendation-title {
            color: #ff4baf;
            margin-bottom: 1.5rem;
            font-size: 1.5em;
            text-align: center;
        }
        .anime-card {
            background-color: #1c1c1e;
            border-radius: 12px;
            padding: 0.5rem;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
            transition: 0.3s ease;
            overflow: hidden;
            text-align: center;
            color: white;
            margin: 0.5rem;
            border: 1px solid rgba(255, 75, 175, 0.2);
        }
        .anime-card:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(255, 75, 175, 0.3);
            border-color: #ff4baf;
        }
        .anime-image {
            border-radius: 10px;
            width: 100%;
            height: 200px;
            object-fit: cover;
            margin-bottom: 0.5rem;
        }
        .anime-title {
            margin: 0;
            font-size: 1.1em;
            font-weight: 600;
            color: white;
        }
        .anime-score {
            font-size: 0.9em;
            color: #ff4baf;
            margin: 0.5rem 0;
        }
        .genre-tag {
            display: inline-block;
            padding: 0.2rem 0.5rem;
            border-radius: 12px;
            font-size: 0.8em;
            margin: 0.2rem;
            background-color: rgba(255, 75, 175, 0.2);
            color: #ff4baf;
        }
        .input-card {
            background-color: #1c1c1e;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(255, 75, 175, 0.2);
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
        }
        .loading-text {
            text-align: center;
            color: #ff4baf;
            font-size: 1.2em;
            margin: 2rem 0;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { opacity: 0.6; }
            50% { opacity: 1; }
            100% { opacity: 0.6; }
        }
    </style>
    """, unsafe_allow_html=True)

# Load anime data
anime_df = load_anime_data()
anime_list = anime_df['name'].tolist()

# Netflix-style recommendation display
def show_netflix_style_recommendations(df):
    # Add background colors based on genre
    df["bg_color"] = df["genre"].apply(genre_to_color)
    
    # Add image URLs
    df["image_url"] = df["name"].apply(get_anime_image)
    
    # Create a container for the recommendations
    container = st.container()
    
    # Create columns for each recommendation
    cols = st.columns(len(df))
    
    # Display each anime in its own card
    for col, row in zip(cols, df.itertuples()):
        with col:
            st.markdown(f"""
            <div class="anime-card" style="background-color: {row.bg_color};">
                <img src="{row.image_url}" class="anime-image" alt="{row.name}" />
                <h5 class="anime-title">{row.name}</h5>
                <p class="anime-score">⭐ {row.final_score:.2f}</p>
                <div class="genre-tags">
                    {''.join([f'<span class="genre-tag">{genre}</span>' for genre in row.genre.split(',')])}
                </div>
            </div>
            """, unsafe_allow_html=True)

# Animated background
components.html("""
<div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
            background: url('https://media.giphy.com/media/xT0xeJpnrWC4XWblEk/giphy.gif') repeat;
            background-size: 150px; opacity: 0.05; z-index: -1;"></div>
""", height=0)

# Hero Banner
st.markdown("""
<div style='text-align: center; margin-top: 20px; margin-bottom: 30px;'>
    <h1 style='font-size: 3em; color: #ff4baf; text-shadow: 0 0 10px rgba(255, 75, 175, 0.5);'>
        🎌 KawaiiRecSys 🎌
    </h1>
    <p style='font-size: 1.2em; color: #cccccc;'>
        Your AI-Powered Anime Bestie 🌸
    </p>
</div>
""", unsafe_allow_html=True)

# Input card
with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    
    # User inputs
    st.markdown('<h2 class="section-title">🔍 Find Your Next Favorite Anime</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        user_id = st.number_input(
            "Enter your user ID",
            min_value=1,
            step=1,
            value=100,
            key="user_id",
            help="Enter a valid user ID to get personalized recommendations"
        )
    with col2:
        selected_anime = st.multiselect(
            "Select anime you like",
            options=anime_list,
            help="Select one or more anime to get recommendations"
        )
    
    # Alpha parameter for hybrid weighting
    alpha = st.slider(
        "Collaborative Filtering Weight",
        min_value=0.0,
        max_value=1.0,
        value=0.6,
        step=0.1,
        help="Adjust the balance between content-based and collaborative filtering"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

if st.button("✨ Get Recommendations ✨", key="recommend_button"):
    if selected_anime:
        with st.spinner("✨ Summoning your anime... ✨"):
            try:
                # Load ratings data
                ratings_df = pd.read_csv(os.path.join(project_root, "data/ratings.csv"))
                
                # Get recommendations
                recs = hybrid_recommend(
                    user_id=user_id,
                    selected_anime=selected_anime,
                    ratings_df=ratings_df,
                    anime_df=anime_df,
                    top_n=5,
                    alpha=alpha
                )
                
                # Dynamic title with character limit and tooltip
                max_len = 60
                if selected_anime:
                    selected_str = ", ".join(selected_anime)
                    display_str = (selected_str[:max_len] + "...") if len(selected_str) > max_len else selected_str
                    st.markdown(f"""
                    <h3 class="recommendation-title" title="{selected_str}">
                        🍿 Your Personalized Picks Based on: <span style="color:#ff4baf;">{display_str}</span>
                    </h3>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <h3 class="recommendation-title">
                        🍿 Your Personalized Picks
                    </h3>
                    """, unsafe_allow_html=True)
                
                # Display Netflix-style recommendations
                show_netflix_style_recommendations(recs)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please select at least one anime.")

# Anime Quote Footer
st.markdown(f"""
<div class="quote-footer">
    📖 {get_random_quote()}
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    pass 