import streamlit as st
import json
import os

# --- USER MANAGEMENT LOGIC ---
# File to store user credentials
USER_FILE = "users.json"

# Initialize user file
def initialize_user_file():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as file:
            json.dump({}, file)

# Load users from the file
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            return json.load(file)
    return {}

# Save users to the file
def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Initialize the user file and load existing users
initialize_user_file()
users = load_users()

# --- RESPONSIVE CUSTOM CSS ---
def add_responsive_styles():
    st.markdown("""
        <style>
            /* General Page Styling */
            .title-text {
                font-size: 40px;
                font-weight: bold;
                color: DodgerBlue;
                text-align: center;
                text-transform: uppercase;
                letter-spacing: 3px;
                margin-top: 30px;
            }
            .subtitle-text {
                font-size: 18px;
                text-align: center;
                color: Tomato;
                margin-bottom: 20px;
            }
            /* Full-Width Buttons */
            div.stButton > button {
                width: 100%;
                background-color: #0B5ED7;
                color: white;
                padding: 12px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            div.stButton > button:hover {
                background-color: #084298;
                transition: 0.3s ease;
            }
            /* Responsive Adjustments */
            @media (max-width: 768px) {
                .title-text {
                    font-size: 30px;
                }
                .subtitle-text {
                    font-size: 16px;
                }
            }
        </style>
    """, unsafe_allow_html=True)

# --- PAGE FUNCTIONS ---

# Home Page
def home():
    add_responsive_styles()
    st.markdown('<div class="title-text">INDIACITYGDP: A VISUALIZATION OF URBAN ECONOMIC METRICS</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">Explore the economic data of Indian cities through visualizations and interactive dashboards.</div>', unsafe_allow_html=True)
    
    # Buttons for Login and Signup
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            st.session_state["page"] = "Login"
            st.rerun()  # Ensure immediate navigation
    with col2:
        if st.button("Signup"):
            st.session_state["page"] = "Signup"
            st.rerun()  # Ensure immediate navigation

# Login Page
def login():
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        if email in users and users[email]["password"] == password:
            st.success("Login Successful! Redirecting...")
            st.session_state["page"] = "Dashboard"
            st.rerun()  # Ensure immediate navigation
        else:
            st.error("Invalid email or password.")
    if st.button("Back to Home"):
        st.session_state["page"] = "Home"
        st.rerun()  # Ensure immediate navigation

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
            st.error("User already exists! Redirecting to Login...")
            st.session_state["page"] = "Login"
            st.rerun()  # Ensure immediate navigation
        elif password != confirm_password:
            st.error("Passwords do not match!")
        else:
            users[email] = {"name": name, "password": password}
            save_users(users)
            st.success("Signup Successful! Redirecting to Home...")
            st.session_state["page"] = "Home"
            st.rerun()  # Ensure immediate navigation
    if st.button("Back to Home"):
        st.session_state["page"] = "Home"
        st.rerun()  # Ensure immediate navigation

# Dashboard Page
def display_dashboard():
    st.title("Power BI Dashboard")
    st.markdown("""
        <div style="max-width: 100%; overflow: hidden;">
            <iframe 
                title="15cities" 
                width="100%" 
                height="500px"
                src="https://app.powerbi.com/view?r=eyJrIjoiZmY4YTE1MjktMDlmMy00ZjU3LWE0NTUtMTY0ZTMxMmMwODA5IiwidCI6ImRmODY3OWNkLWE4MGUtNDVkOC05OWFjLWM4M2VkN2ZmOTVhMCJ9" 
                frameborder="0" 
                allow="fullscreen">
            </iframe>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Signout"):
        st.session_state["page"] = "Home"
        st.rerun()  # Ensure immediate navigation

# --- MAIN APP ---
def main():
    # Set default page to "Home"
    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    # Navigation Logic
    if st.session_state["page"] == "Home":
        home()
    elif st.session_state["page"] == "Login":
        login()
    elif st.session_state["page"] == "Signup":
        signup()
    elif st.session_state["page"] == "Dashboard":
        display_dashboard()

# Run the app
if __name__ == "__main__":
    main()
