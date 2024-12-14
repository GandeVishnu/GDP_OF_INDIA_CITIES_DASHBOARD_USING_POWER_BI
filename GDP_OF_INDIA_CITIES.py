import streamlit as st
import json
import os

# File to store user credentials
USER_FILE = "users.json"

def initialize_user_file():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as file:
            json.dump({}, file)  # Initialize an empty dictionary

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            return json.load(file)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

initialize_user_file()
users = load_users()

# Responsive Styling
def add_responsive_styles():
    st.markdown("""
        <style>
            /* General styling */
            .title-text {
                font-size: 40px;
                font-weight: bold;
                color: DodgerBlue;
                text-align: center;
                text-transform: uppercase;
                letter-spacing: 3px;
            }
            .subtitle-text {
                font-size: 18px;
                text-align: center;
                color: Tomato;
                padding-bottom: 30px;
            }

            /* Responsive adjustments */
            @media (max-width: 768px) {
                .title-text {
                    font-size: 30px;
                }
                .subtitle-text {
                    font-size: 14px;
                }
                .stButton>button {
                    width: 100%; /* Full-width buttons on smaller screens */
                }
            }
        </style>
    """, unsafe_allow_html=True)

# Home Page
def home():
    add_responsive_styles()
    st.markdown('<p class="title-text">IndiaCityGDP: A Visualization of Urban Economic Metrics</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Explore the economic data of Indian cities through visualizations and interactive dashboards.</p>', unsafe_allow_html=True)

    # Use responsive columns
    col1, col2 = st.columns(2)
    if col1.button("Login"):
        st.session_state["page"] = "Login"
    if col2.button("Signup"):
        st.session_state["page"] = "Signup"

# Login Page
def login():
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if email in users and users[email]["password"] == password:
            st.success("Login Successful!")
            st.session_state["page"] = "Dashboard"
        else:
            st.error("Invalid email or password.")
    if st.button("Home"):
        st.session_state["page"] = "Home"

# Signup Page
def signup():
    st.subheader("Signup")
    name = st.text_input("Name", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Re-enter Password", type="password", key="signup_confirm_password")
    
    if st.button("Signup"):
        if not name or not email or not password or not confirm_password:
            st.error("All fields are required.")
        elif email in users:
            st.error("User already exists! Redirecting to home...")
            st.session_state["page"] = "Home"
        elif password != confirm_password:
            st.error("Passwords do not match!")
        else:
            users[email] = {
                "name": name,
                "email": email,
                "password": password
            }
            save_users(users)
            st.success("Signup Successful! Redirecting to home...")
            st.session_state["page"] = "Home"

    if st.button("Home"):
        st.session_state["page"] = "Home"

# Dashboard Page
def display_dashboard():
    st.title("Power BI Dashboard")
    st.markdown(
        """
        <div style="max-width: 100%; overflow: hidden;">
            <iframe 
                title="15cities" 
                width="100%" 
                height="400px" 
                src="https://app.powerbi.com/view?r=eyJrIjoiZmY4YTE1MjktMDlmMy00ZjU3LWE0NTUtMTY0ZTMxMmMwODA5IiwidCI6ImRmODY3OWNkLWE4MGUtNDVkOC05OWFjLWM4M2VkN2ZmOTVhMCJ9" 
                frameborder="0" 
                allow="fullscreen">
            </iframe>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Signout"):
        st.session_state["page"] = "Home"

# Main App Logic
def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    if st.session_state["page"] == "Home":
        home()
    elif st.session_state["page"] == "Login":
        login()
    elif st.session_state["page"] == "Signup":
        signup()
    elif st.session_state["page"] == "Dashboard":
        display_dashboard()

if __name__ == "__main__":
    main()
