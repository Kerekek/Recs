import streamlit as st
import pandas as pd
from database import init_db, create_animetable, show_user_list, add_animedata, registered_title_check
from authentication import show_sign_in, show_sign_up
from Home_page import show_home_page

# Initialize the database and table
con, cur = init_db()

# Importing expected columns and checking
data = pd.read_csv("C:/Users/alaca/Desktop/1/REcs_of_D_kerekek/Recs/REcs_of_D_trydata3.csv")
data_sorted = data.sort_values(by='Scoredby', ascending=False)

expected_columns = ['Title', 'Genre', 'Synopsis', 'Type', 'Studio', 'Rating', 'Scoredby', 'Episodes', 'Source', 'Aired', 'Image_url']
missing_columns = [col for col in expected_columns if col not in data_sorted.columns]
if missing_columns:
    st.error(f"Missing columns in the csv file: {missing_columns}")
    st.stop()

st.set_page_config(page_title="Movie Recommender", layout="wide")

# Initialize session state variables
if "watched_movies" not in st.session_state:
    st.session_state.watched_movies = []
if "tags" not in st.session_state:
    st.session_state.tags = {row['Title']: "" for _, row in data_sorted.iterrows()}
if "show_watched_list" not in st.session_state:
    st.session_state.show_watched_list = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "page" not in st.session_state:
    st.session_state.page = "Sign In"

# Page routing
if st.session_state.page == "Sign In":
    show_sign_in(cur)
elif st.session_state.page == "Sign Up":
    show_sign_up(cur)
else:
    show_home_page(st.session_state.current_user[0], cur, data_sorted, con)

# Styling and layout
st.markdown("""
    <style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
    .main {
        background-color: #333333;
        color: #FFFFFF;
    }
    .stTextInput input {
        background-color: #333333;
        color: #FFFFFF;
    }
    .stButton button {
        background-color: #FF9900;
        color: #000000;
        width: 100%;
    }
    .header-container {
        background-color: #CC5500;
        padding: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .header-container div {
        color: #FFFFFF;
    }
    .search-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }
    .search-input {
        width: 50%;
        padding: 10px;
        border-radius: 5px;
        border: none;
    }
    .movie-container {
        background-color: #333333;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .movie-title {
        font-size: 24px;
        font-weight: bold;
    }
    .movie-details {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .movie-image {
        flex: 1;
        max-width: 200px;
    }
    .movie-info {
        flex: 2;
    }
    .tags-container {
        margin-top: 20px;
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .tag {
        background-color: #CC5500;
        padding: 5px 10px;
        border-radius: 5px;
    }
    .similar-movies {
        margin-top: 20px;
    }
    .similar-movies img {
        margin-right: 10px;
        border-radius: 5px;
    }
    .edit-link {
        margin-top: 10px;
        color: #FF9900;
        cursor: pointer;
    }
    .watched-list-button {
        background-color: #FF9900;
        color: #000000;
        padding: 10px;
        border: none;
        cursor: pointer;
    }
    .rate-button {
        background-color: #FF9900;
        color: #000000;
        padding: 5px 10px;
        border: none;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)