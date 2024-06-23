import streamlit as st
import pandas as pd
import numpy as np
import json

import requests
import settings

st.set_page_config(page_title = "Happy Coloring : Admin Page", page_icon="🏦")


def Management():
    st.title("User List")
    r = requests.get("http://localhost:8000/api/users")
    #st.write(r)
    _jlist = r.json()

    df = pd.DataFrame(data=_jlist)
    st.dataframe(df, width=1000)


def PrintStat():
    st.title("Print Log")
    myobj = {'id': 0 }
    r = requests.get("http://localhost:8000/api/logs", json=myobj)
    _jlist = r.json()

    df = pd.DataFrame(data=_jlist)
    st.dataframe(df)

def PictureStat():
    st.title("Picture List")
    myobj = {'id': 0 }
    r = requests.get("http://localhost:8000/api/pictures", json=myobj)
    _jlist = r.json()

    df = pd.DataFrame(data=_jlist)
    st.dataframe(df)

def ChangeProfile():
    st.title("Log out")

def SetProfile():
    st.title("ChangeProfile")

def InitialPage():
    #st.sidebar.title('Author')

    pg = st.navigation({
        "Admin" : [st.Page(Management, title="Users"), st.Page(PictureStat, title="Pictures"), st.Page(PrintStat, title="Log")],
        "Account" : [st.Page(ChangeProfile, title="Log out"), st.Page(SetProfile, title="Setting")]
    })

    pg.run()


def Admin():

    InitialPage()



Admin()
