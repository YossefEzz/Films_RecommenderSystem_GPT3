import streamlit as st
import pandas as pd
import pickle
import os
import base64

# Load the data
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'cosine_sim_df_32.pickle')
    with open(file_path, 'rb') as f:
        cosine_sim_df = pickle.load(f)
    return cosine_sim_df

# Function to get recommendations
def get_recommendations(title, cosine_sim_df, top_n):
    if title not in cosine_sim_df.index:
        return ["Film not found in the database."]
    sim_scores = cosine_sim_df[title].sort_values(ascending=False)
    top_n_recommendations = sim_scores.iloc[1:top_n+1].index.tolist()
    return top_n_recommendations

# Function to load and encode the logo image
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Main function to run the Streamlit app
def main():
    st.set_page_config(page_title="Azure Recommender System", layout="wide")
    
    # Custom CSS for styling
    logo_path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'proAr.png')
    logo_base64 = get_base64_image(logo_path)
    
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: #000814;  /* Darker navy, almost black */
            color: white;
        }}
        .stButton>button {{
            background-color: #4CAF50;
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
            background-color: #45a049;
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
        </style>
        """, unsafe_allow_html=True)

    # Add watermark div outside of style tag
    st.markdown(f"""
        <div class="watermark">
            <img src="data:image/png;base64,{logo_base64}" alt="Watermark">
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>Azure Recommender System</h1>", unsafe_allow_html=True)
    st.write("This is a simple content-based recommender system for films created for DEPI project.")

    # Load data
    cosine_sim_df = load_data()

    # Get list of film titles
    film_titles = cosine_sim_df.index.tolist()

    # User input for film name with autocomplete
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
        # Get recommendations
        recommendations = get_recommendations(film_name, cosine_sim_df, top_n)
        
        # Display recommendations
        st.write(f"Top {top_n} recommendations for '{film_name}':")
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")


if __name__ == "__main__":
    main()