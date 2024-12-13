import streamlit as st
import json
import os

# File to store user credentials
USER_FILE = "users.json"

# Load existing users from the file or initialize an empty dictionary
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            return json.load(file)
    return {}

# Save users to the file
def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Initialize users dictionary
users = load_users()

# Function to display Power BI dashboard
def display_dashboard():
    st.title("Power BI Dashboard")
    st.markdown(
        """
    <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
        <iframe 
            title="15cities" 
            width="100%" 
            height="100%" 
            src="https://app.powerbi.com/view?r=eyJrIjoiZmY4YTE1MjktMDlmMy00ZjU3LWE0NTUtMTY0ZTMxMmMwODA5IiwidCI6ImRmODY3OWNkLWE4MGUtNDVkOC05OWFjLWM4M2VkN2ZmOTVhMCJ9" 
            frameborder="0" 
            allowFullScreen="true">
        </iframe>
    </div>
        """,
        unsafe_allow_html=True,
    )
    # Add spacing
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("Signout", key="signout_button"):
        st.session_state["page"] = "Home"

# Login Page
def login():
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        if email in users and users[email]["password"] == password:
            st.success("Login Successful!")
            st.session_state["page"] = "Dashboard"
        else:
            st.error("Invalid email or password.")

    # Add Home button
    if st.button("Home", key="login_home_button"):
        st.session_state["page"] = "Home"

# Signup Page
def signup():
    st.subheader("Signup")
    name = st.text_input("Name", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    confirm_password = st.text_input("Re-enter Password", type="password", key="signup_confirm_password")
    
    if st.button("Signup", key="signup_button"):
        if not name or not email or not password or not confirm_password:
            st.error("All fields are required.")
        elif email in users:
            st.error("User already exists! Redirecting to home...")
            st.session_state["page"] = "Home"
        elif password != confirm_password:
            st.error("Passwords do not match!")
        else:
            # Save the user's details (name, email, and password)
            users[email] = {
                "name": name,
                "email": email,
                "password": password  # Consider hashing the password for security
            }
            save_users(users)
            st.success("Signup Successful! Redirecting to home...")
            st.session_state["page"] = "Home"
    
    if st.button("Home", key="signup_home_button"):
        st.session_state["page"] = "Home"

# Main Page
def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    if st.session_state["page"] == "Home":
        # Custom styles for the Home page header
        st.markdown(""" 
            <style>
                .title-text {
                    font-size: 40px;
                    font-weight: bold;
                    color: DodgerBlue;
                    padding: center;
                    text-transform: uppercase;
                    letter-spacing: 3px;
                }
                .subtitle-text {
                    font-size: 18px;
                    text-align: center;
                    color: Tomato;
                    padding-bottom: 30px;
                }
                @media (max-width: 768px) {
                    .title-text {
                        font-size: 30px;
                    }
                    .subtitle-text {
                        font-size: 14px;
                    }
                }
                /* Responsive layout for buttons */
                @media (max-width: 600px) {
                    .stButton>button {
                        width: 100%;
                    }
                }
            </style>
        """, unsafe_allow_html=True)

        # Title and description with creative text
        st.markdown('<p class="title-text">IndiaCityGDP: A Visualization of Urban Economic Metrics</p>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle-text">Explore the economic data of Indian cities through visualizations and interactive dashboards.</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        if col1.button("Login", key="main_login_button"):
            st.session_state["page"] = "Login"
        if col2.button("Signup", key="main_signup_button"):
            st.session_state["page"] = "Signup"
    
    elif st.session_state["page"] == "Login":
        login()

    elif st.session_state["page"] == "Signup":
        signup()
    
    elif st.session_state["page"] == "Dashboard":
        display_dashboard()

# App execution
if __name__ == "__main__":
    main()
