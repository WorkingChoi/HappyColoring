import base64
import io
import os
from pathlib import Path

import numpy as np
from PIL import Image

import streamlit as st
import pandas as pd
from io import StringIO

@st.cache_data
def _encode_numpy(img):
    pil_img = Image.fromarray(img)
    buffer = io.BytesIO()
    pil_img.save(buffer, format="JPEG")
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/jpeg;base64, {encoded}"

def Management():
    st.title("My Picture")

def NewPicture():
    st.title("Eroll Picture")

    uploaded_files = st.file_uploader("Choose a JPG file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        #st.write(bytes_data)

def AllList():
    st.title("AllList")

def PrintStat():
    st.title("PrintStat")

def PictureStat():
    st.title("PictureStat")

def ChangeProfile():
    st.title("ChangeProfile")

def UserFav():
    st.title("User : Favorite")

def UserSearch():
    st.title("User : Search")

def UserStat():
    st.title("User : Statistic")

def AdminUserList():
    st.title("Admin : User List")

def AdminPictureList():
    st.title("Admin : Picture List")

def InitialPage(role):
    st.sidebar.title(str(role).upper())

    page_dict = {}
    role = st.session_state.role

    logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
    settings = st.Page("settings.py", title="Settings", icon=":material/settings:")

    user_1 = st.Page(UserFav, title="Favorite")
    user_2 = st.Page(UserSearch, title="Search")
    user_3 = st.Page(UserStat, title="Statistic")

    author_1 = st.Page(Management, title="Manage")
    author_2 = st.Page(NewPicture, title="New")
    author_3 = st.Page(PrintStat, title="Statistic")

    admin_1 = st.Page(AdminUserList, title="Users")
    admin_2 = st.Page(AdminPictureList, title="Pictures")

    account_pages = [logout_page, settings]
    user_pages = [user_1, user_2, user_3]
    author_pages = [author_1, author_2, author_3]
    admin_pages = [admin_1, admin_2]

    st.write(role)

    if role == "author":
        page_dict["Author"] = author_pages
    elif role == "admin":
        page_dict["Admin"] = admin_pages
    elif role == "user":
        page_dict["User"] = user_pages

    print('InitialPage : ' + role)
    pg = st.navigation({"Account": account_pages} | page_dict)
    # if len(page_dict) > 0:
    #     pg = st.navigation({"Account": account_pages} | page_dict)
    # else:
    #     pg = st.navigation([st.Page(main.login)])
    
    pg.run()

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

        print(role)

        st.write(role)
        st.session_state.role = role
        InitialPage(role)

def logout():
    st.session_state.role = None
    st.rerun()

def run():
    role = st.session_state.role
    st.sidebar.header(role)
    InitialPage(role)

st.set_page_config(page_title = "Login Page", page_icon="🏦")

if "role" not in st.session_state:
    st.session_state.role = None

login()
