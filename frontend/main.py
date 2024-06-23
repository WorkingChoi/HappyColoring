import yaml
from yaml.loader import SafeLoader

import streamlit as st

if "role" not in st.session_state:
    st.session_state.role = None

if "grade" not in st.session_state:
    st.session_state.grade = None

# Retrieve the role from Session State to initialize the widget
st.session_state._role = st.session_state.role

def set_role():
    # Callback function to save the role selection to Session State
    st.session_state.role = st.session_state._role


def login():
    st.header("Log in")
    email = st.text_input("email")
    pwd = st.text_input("password", type="password")
    if st.button("Log in"):
        if email[:5] == "admin" :
            role = "admin"
        elif email[:6] == "author" :
            role = "author"
        else:
            role = "user"
            
        st.session_state.role = role

        st.write(role)

        st.switch_page("pages/" + role + ".py")
        st.rerun()


def logout():
    st.session_state.role = None
    st.rerun()

login()
