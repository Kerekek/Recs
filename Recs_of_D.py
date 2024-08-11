import pandas as pd
import streamlit as st

import sqlite3
con = sqlite3.connect("Recs_of_D.db")
cur = con.cursor()

# Importing expected columns and checking
#file_path = 
data = pd.read_csv("C:/Users/alaca/Desktop/1/REcs_of_D_kerekek/Recs/REcs_of_D_trydata3.csv")

expected_columns = ['Title', 'Genre', 'Synopsis', 'Type', 'Studio', 'Rating', 'Scoredby', 'Episodes', 'Source', 'Aired', 'Image_url']
missing_columns = [col for col in expected_columns if col not in data.columns]
if missing_columns:
    st.error(f"Missing columns in the csv file: {missing_columns}")
    st.stop()

st.set_page_config(page_title="Movie Recommender", layout="wide")

# Initialize session state variables
if "watched_movies" not in st.session_state:
    st.session_state.watched_movies = []
if "tags" not in st.session_state:
    st.session_state.tags = {row['Title']: "" for _, row in data.iterrows()}
if "show_watched_list" not in st.session_state:
    st.session_state.show_watched_list = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "page" not in st.session_state:
    st.session_state.page = "Sign In"

# Function to toggle watched list display
def toggle_watched_list():
    st.session_state.show_watched_list = not st.session_state.show_watched_list

def create_animetable():
    cur.execute('CREATE TABLE IF NOT EXISTS movietable(username TEXT, title TEXT, rating INTEGER, state INTEGER)')
    con.commit()
def add_animedata(username,title,rating,state):
    cur.execute('INSERT INTO movietable(username,title,rating,state) VALUES (?,?,?,?)', (username,title,rating,state))
    con.commit()
def show_user_list(username):
    cur.execute('SELECT * FROM movietable WHERE username =?', (username,))
    data = cur.fetchall()
    return data

# Showing home page
def show_home_page(user_name):
    st.markdown(f"""
        <div class="header-container">
            <div>{user_name}</div>
            <div><button onclick="document.location.reload()">Mylist</button></div>
            <div><button onclick="document.location.reload()">Sign Out</button></div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Watched List", key="watched-list-toggle"):
        toggle_watched_list()
    
    if st.session_state.show_watched_list:
        st.subheader('Watched Movies')
        watched_list = show_user_list(user_name)
        sorted_animes = sorted(watched_list, key=lambda x: -x[2])
        for anime in sorted_animes:
            st.write(f"{anime[1]} - {anime[2]} stars")
            if st.button(f'Remove {anime[1]} from Watched List', key=f'remove-{anime[1]}'):
                st.session_state.watched_movies = [m for m in st.session_state.watched_movies if m['title'] != anime[1]]
                st.success(f'{anime[1]} removed from watched list!')
        return
    
    search_query = st.text_input("Search for a movie", key="search_input").lower()
    filtered_data = data[data['Title'].str.lower().str.contains(search_query)]

    # Page size is adjustable
    page_size = 12
    # Calculate the total number of pages
    total_pages = len(filtered_data) // page_size + 1
    # Get the current page number from user input
    st.write("Change Page")
    current_page = st.number_input("Page", min_value=1, max_value=total_pages,format="%d",placeholder="Load more")
    # Calculate the start and end indices for the current page
    start_index = (current_page - 1) * page_size
    end_index = min(start_index + page_size, len(filtered_data))

    # Display the data for the current page
    for index in range(start_index, end_index):
        row = filtered_data.iloc[index]
        st.markdown(f"""
            <div class="movie-container">
                <div class="movie-title">{row['Title']}</div>
                <div class="movie-details">
                    <div class="movie-image">
                        <img src="{row['Image_url']}" alt="Movie Image" width="200">
                    </div>
                    <div class="movie-info">
                        <div>{row['Rating']} stars</div>
                        <div>Genres: {row['Genre']}</div>
                        <div>Synopsis: {row['Synopsis']}</div>
                        <div>Type: {row['Type']}</div>
                        <div>Studio: {row['Studio']}</div>
                        <div>Scored by: {row['Scoredby']}</div>
                        <div>Episodes: {row['Episodes']}</div>
                        <div>Source: {row['Source']}</div>
                        <div>Aired: {row['Aired']}</div>
                        <div class="edit-link" onClick="document.getElementById('edit-form-{index}').style.display = 'block';">Edit</div>
                    </div>
                </div>
                <div id="edit-form-{index}" style="display:none;">
                    <form>
                        <label for="tags">Tags:</label><br>
                        <input type="text" id="tags" name="tags" value="{st.session_state.tags[row['Title']]}"><br>
                        <input type="submit" value="Save">
                    </form>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Rating system
        create_animetable()
        rating = st.selectbox(f'Rate {row["Title"]}:', [1, 2, 3, 4, 5], key=f'rating-{index}')
        states = ["Continuing","Completed","On-Hold","Dropped","Plan to Watch"]
        statebox = st.selectbox(f"State of {row['Title']}",states, key=f'state_{index}')
        state_index = states.index(statebox)
        if st.button(f'Save Rating and State {row["Title"]}', key=f'save-{index}'):
            add_animedata(st.session_state.current_user[0],row["Title"],rating,state_index)
            st.success('Rating saved and movie marked as watched!')
    # if end_index < len(filtered_data):
    #     if st.button("Load more"):
    #         current_page += 1
    # else:
    #     st.write("No more data to load.")


def create_usertable():
    cur.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,email TEXT, password TEXT)')
    
def add_userdata(username,email,password):
    cur.execute('INSERT INTO userstable(username,email, password) VALUES (?,?,?)', (username,email,password))
    con.commit()

def login_user(username,password):
    cur.execute('SELECT * FROM userstable WHERE username =? AND password =? ', (username,password))
    data = cur.fetchall()
    return data

def view_all_users():
    cur.execute('SELECT * FROM userstable')
    data = cur.fetchall()
    return data

# Sign in and sign up
def show_sign_in():
    st.markdown(f'<i class="fa-solid fa-lock fa-3x" style="color: #FF9900;"></i>', unsafe_allow_html=True)
    st.title("Sign In")
    ID_input = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        create_usertable()
        result = login_user(ID_input, password)
        if result:
            st.session_state.page = "Home"
            st.session_state.current_user = result[0]  # Assuming the first element is the username
            #st.success(f"Welcome, {result[0]}!")
        else:
            st.error("Invalid username or password")
    if st.button("Create Account"):
        st.session_state.page = "Sign Up"

def show_sign_up():
    st.markdown(f'<i class="fa-solid fa-lock fa-3x" style="color: #FF9900;"></i>', unsafe_allow_html=True)
    st.title("Sign Up")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    terms = st.checkbox("I accept the Terms of Service and Privacy Policy")
    if st.button("Create Account"):
        if terms:
            create_usertable()
            existing_users = view_all_users()
            emails = [user[1] for user in existing_users]
            usernames = [user[0] for user in existing_users]

            if email in emails:
                st.error("Email already registered")
            elif username in usernames:
                st.error("Username already taken")
            else:
                add_userdata(username, email, password)
                st.session_state.page = "Home"
                st.session_state.current_user = username
                st.success(f"Account created for {username}!")
        else:
            st.error("You must accept the terms to create an account.")
    if st.button("Sign In"):
        st.session_state.page = "Sign In"

# Page routing
if st.session_state.page == "Sign In":
    show_sign_in()
elif st.session_state.page == "Sign Up":
    show_sign_up()
else:
    st.write(f"Welcome {st.session_state.current_user[0]}!")
    #st.write(f"Current User: {st.session_state.current_user}")
    show_home_page(st.session_state.current_user[0])

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