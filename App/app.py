import streamlit as st
import pandas as pd
import pickle
import os
import base64
import requests

# Fetch genre list from TMDB API
def fetch_genres():
    api_key = "b46555459e2e7dfbe1657f14b1cbe511"  # Your TMDB API key
    genre_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US"
    response = requests.get(genre_url)

    if response.status_code == 200:
        genres_data = response.json()
        genres_dict = {genre['id']: genre['name'] for genre in genres_data['genres']}
        return genres_dict
    else:
        st.error(f"Error fetching genres from TMDB API: {response.status_code}")
        return {}

# Load the data
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'cosine_sim_df_32.pickle')
    with open(file_path, 'rb') as f:
        cosine_sim_df = pickle.load(f)
    return cosine_sim_df

# Function to get recommendations and remove duplicates
def get_recommendations(title, cosine_sim_df, top_n):
    if title not in cosine_sim_df.index:
        return ["Film not found in the database."]
    
    # Get similarity scores
    sim_scores = cosine_sim_df[title].sort_values(ascending=False)
    
    # Extract top N recommendations and ensure they are unique
    top_n_recommendations = list(dict.fromkeys(sim_scores.iloc[1:top_n + 1].index.tolist()))  # Remove duplicates
    
    return top_n_recommendations


# Function to load and encode the logo image
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Function to fetch movie details from TMDB API
def fetch_movie_details(movie_title, genres_dict):
    api_key = "b46555459e2e7dfbe1657f14b1cbe511"  # Your TMDB API key
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            movie_data = data['results'][0]
            poster_path = movie_data.get('poster_path')
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else None
            overview = movie_data.get('overview', 'No overview available.')
            rating = movie_data.get('vote_average', 'No rating available.')
            release_date = movie_data.get('release_date', 'Unknown')
            genre_ids = movie_data.get('genre_ids', [])
            genres = [genres_dict.get(genre_id, 'Unknown') for genre_id in genre_ids]  # Map genre IDs to names
            movie_id = movie_data.get('id', '')
            return full_path, overview, rating, release_date, genres, movie_id
        else:
            return None, None, None, None, None, None
    else:
        st.error(f"Error fetching data from TMDB API: {response.status_code}")
        return None, None, None, None, None, None


# Function to fetch movie trailer from TMDB API and handle missing trailers
def fetch_movie_trailer(movie_id):
    api_key = "b46555459e2e7dfbe1657f14b1cbe511"  # Your TMDB API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            for video in data['results']:
                if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                    youtube_url = f"https://www.youtube.com/watch?v={video['key']}"
                    # Add basic check for video validity (Optional improvement)
                    if requests.head(youtube_url).status_code == 200:
                        return youtube_url
                    else:
                        return None  # Trailer link is broken
        return None
    else:
        st.error(f"Error fetching trailer from TMDB API: {response.status_code}")
        return None


# Function to create a trailer button
def create_trailer_button(trailer_url):
    if trailer_url:
        return f"""
        <a href="{trailer_url}" target="_blank" class="trailer-button">
            <img src="https://img.icons8.com/ios-filled/50/000000/play--v1.png" width="24" height="24" style="vertical-align: middle;"/>
            <span>Watch Trailer</span>
        </a>
        """
        
    else:
        return "<span>No trailer available.</span>"

# Main function to run the Streamlit app
def main():
    st.set_page_config(page_title="Azure Recommender System", layout="wide")

    # Load genre data
    genres_dict = fetch_genres()

    # Custom CSS for styling and button color change
    logo_path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'proAr.png')
    logo_base64 = get_base64_image(logo_path)

    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(135deg, #020024, #090979, #00d4ff);
            color: white;
        }}
        .stButton>button {{
            background-color: #000;
            color: white;
            border: none;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 12px;
        }}
        .stButton>button:hover {{
            background-color: #104E8B; 
        }}
        .stSelectbox, .stMultiSelect {{
            color: black;
        }}
        .watermark {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            opacity: 0.1;
            pointer-events: none;
            z-index: 9999;
            width: 45%;
            height: auto;
        }}
        .button-container {{
            display: flex;
            justify-content: center;
            gap: 10px;
        }}
        .trailer-button {{
            text-decoration: none;
            color: #fff;
            padding: 8px 16px;
            border-radius: 8px;
            background-color: #000; 
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}
        .trailer-button:hover {{
            background-color:  #104E8B ;
        }}
        .trailer-button img {{
            filter: brightness(0) invert(1);
        }}
        </style>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <div class="watermark">
            <img src="data:image/png;base64,{logo_base64}" alt="Watermark">
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>Azure Recommender System</h1>", unsafe_allow_html=True)

    # Load data
    cosine_sim_df = load_data()

    # Get list of film titles
    film_titles = cosine_sim_df.index.tolist()

    # User input for film name
    film_name = st.selectbox("Enter a film name:", film_titles)

    # Dropdown for number of recommendations
    top_n = st.selectbox("Select number of recommendations:", list(range(1, 11)))

    # Centered buttons for running and clearing
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        run_button = st.button("Run")
    with col2:
        clear_button = st.button("Clear")
    st.markdown('</div>', unsafe_allow_html=True)

    if clear_button:
        st.session_state.clear()
        st.rerun()

    if run_button and film_name:
        # Display the movie user searched for
        st.subheader(f"Movie You Searched For: {film_name}")
        poster_url, overview, rating, release_date, genres, movie_id = fetch_movie_details(film_name, genres_dict)

        if poster_url:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(poster_url, width=150)
            with col2:
                st.markdown(f"**{film_name}**")
                st.write(f"**Rating:** {rating} ⭐")
                st.write(f"**Release Date:** {release_date}")
                st.write(f"**Genres:** {', '.join(genres)}")
                st.write(f"**Overview:** {overview}")

            # Fetch and display the trailer
            trailer_url = fetch_movie_trailer(movie_id)
            st.markdown(create_trailer_button(trailer_url), unsafe_allow_html=True)
            st.markdown("---")
        else:
            st.write(f"{film_name} (No poster available)")

        # Get recommendations
        recommendations = get_recommendations(film_name, cosine_sim_df, top_n)

        if recommendations == ["Film not found in the database."]:
            st.warning(f"No recommendations found for '{film_name}'. Please try another movie.")
        else:
            # Display recommendations with posters, information, and trailers
            st.write(f"Top {top_n} recommendations for '{film_name}':")
            for i, movie in enumerate(recommendations, 1):
                poster_url, overview, rating, release_date, genres, movie_id = fetch_movie_details(movie, genres_dict)

                if poster_url:
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.image(poster_url, width=150)
                    with col2:
                        st.markdown(f"**{movie}**")
                        st.write(f"**Rating:** {rating} ⭐")
                        st.write(f"**Release Date:** {release_date}")
                        st.write(f"**Genres:** {', '.join(genres)}")
                        st.write(f"**Overview:** {overview}")

                    # Fetch and display the trailer for each recommendation
                    trailer_url = fetch_movie_trailer(movie_id)
                    st.markdown(create_trailer_button(trailer_url), unsafe_allow_html=True)
                    st.markdown("---")

                else:
                    st.write(f"{i}. {movie} (No poster available)")

if __name__ == "__main__":
    main()
