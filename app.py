import streamlit as st
from database import init_db, add_user, verify_user

st.set_page_config(page_title="Resume Extractor & Job Portal", page_icon="📄", layout="wide")

# Initialize Database
init_db()

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Background Styling
st.markdown("""
    <style>
        body {background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%); color: white;}
        .stApp {background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);}
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            background-color: #f0f4ff; color: black; border-radius: 10px; padding: 8px;
        }
        .stButton>button {
            background-color: #ff6f61; color: white; border-radius: 8px; padding: 10px 20px; font-weight: bold;
        }
        .stButton>button:hover {background-color: #ff3b2e;}
    </style>
""", unsafe_allow_html=True)

if not st.session_state["logged_in"]:
    tab1, tab2 = st.tabs(["🔑 Login", "🆕 Sign Up"])

    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if verify_user(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success("✅ Logged in successfully!")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

    with tab2:
        new_username = st.text_input("New Username", key="signup_username")
        new_password = st.text_input("New Password", type="password", key="signup_password")
        if st.button("Sign Up"):
            try:
                add_user(new_username, new_password)
                st.success("✅ Account created successfully! Please log in.")
            except:
                st.error("⚠ Username already exists")
else:
    st.sidebar.success(f"Welcome {st.session_state['username']}")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

    st.title("📄 Resume Extractor & Job Portal")
    st.write("Navigate to the sidebar and open **Resume Extractor** to upload and apply for jobs.")
