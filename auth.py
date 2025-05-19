import streamlit as st
import pandas as pd
import os

USER_FILE = "users.csv"

def init_user_db():
    if not os.path.exists(USER_FILE):
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(USER_FILE, index=False)

def register():
    st.title("Register")
    username = st.text_input("Choose a username", key="reg_user")
    password = st.text_input("Choose a password", type="password", key="reg_pass")
    if st.button("Register"):
        df = pd.read_csv(USER_FILE)
        if username in df["username"].values:
            st.error("Username already exists!")
        elif username and password:
            df = df.append({"username": username, "password": password}, ignore_index=True)
            df.to_csv(USER_FILE, index=False)
            st.success("Registration successful! Please log in.")
            st.session_state["menu"] = "🔑 Login"  # Redirect to login
        else:
            st.warning("Please enter both username and password.")

def login():
    st.title("Login")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        df = pd.read_csv(USER_FILE)
        if ((df["username"] == username) & (df["password"] == password)).any():
            st.session_state["logged_in"] = True
            st.session_state["current_user"] = username
            st.success("Login successful! Redirecting to app...")
            st.session_state["menu"] = "📈 App"  # Redirect to app
        else:
            st.error("Invalid username or password.")