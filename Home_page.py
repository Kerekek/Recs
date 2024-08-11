import streamlit as st
from database import create_animetable, show_user_list, add_animedata, registered_title_check

def toggle_watched_list():
    st.session_state.show_watched_list = not st.session_state.show_watched_list

def show_home_page(user_name, cur, data_sorted, con):
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
        watched_list = show_user_list(cur,user_name)
        sorted_animes = sorted(watched_list, key=lambda x: -x[2])
        for anime in sorted_animes:
            st.write(f"{anime[1]} - {anime[2]} stars")
            if st.button(f'Remove {anime[1]} from Watched List', key=f'remove-{anime[1]}'):
                st.session_state.watched_movies = [m for m in st.session_state.watched_movies if m['title'] != anime[1]]
                st.success(f'{anime[1]} removed from watched list!')
        return
    
    search_query = st.text_input("Search for a movie", key="search_input").lower()
    filtered_data = data_sorted[data_sorted['Title'].str.lower().str.contains(search_query)]

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
        create_animetable(cur,con)
        rating = st.selectbox(f'Rate {row["Title"]}:', [1, 2, 3, 4, 5], key=f'rating-{index}')
        states = ["Continuing","Completed","On-Hold","Dropped","Plan to Watch"]
        statebox = st.selectbox(f"State of {row['Title']}",states, key=f'state_{index}')
        state_index = states.index(statebox)
        title_check = registered_title_check(cur,user_name,row["Title"])
        if title_check:
            return
        else:
            if st.button(f'Save Rating and State {row["Title"]}', key=f'save-{index}'):
                add_animedata(cur,con,user_name,row["Title"],rating,state_index)
                st.success('Rating saved and movie marked as watched!')
    # if end_index < len(filtered_data):
    #     if st.button("Load more"):
    #         current_page += 1
    # else:
    #     st.write("No more data to load.")