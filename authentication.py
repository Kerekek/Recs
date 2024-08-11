import streamlit as st
from database import create_usertable, login_user, add_userdata, view_all_users

def show_sign_in(cur):
    st.markdown(f'<i class="fa-solid fa-lock fa-3x" style="color: #FF9900;"></i>', unsafe_allow_html=True)
    st.title("Sign In")
    ID_input = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        create_usertable(cur)
        result = login_user(cur, ID_input, password)
        if result:
            st.session_state.page = "Home"
            st.session_state.current_user = result[0]
        else:
            st.error("Invalid username or password")
    if st.button("Create Account"):
        st.session_state.page = "Sign Up"

def show_sign_up(cur):
    st.markdown(f'<i class="fa-solid fa-lock fa-3x" style="color: #FF9900;"></i>', unsafe_allow_html=True)
    st.title("Sign Up")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    terms = st.checkbox("I accept the Terms of Service and Privacy Policy")
    if st.button("Create Account"):
        if terms:
            create_usertable(cur)
            existing_users = view_all_users(cur)
            emails = [user[1] for user in existing_users]
            usernames = [user[0] for user in existing_users]

            if email in emails:
                st.error("Email already registered")
            elif username in usernames:
                st.error("Username already taken")
            else:
                add_userdata(cur, username, email, password)
                st.session_state.page = "Home"
                st.session_state.current_user = username
                st.success(f"Account created for {username}!")
        else:
            st.error("You must accept the terms to create an account.")
    if st.button("Sign In"):
        st.session_state.page = "Sign In"