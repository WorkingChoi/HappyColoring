import base64
import io
import os

import streamlit as st

import pandas as pd
import numpy as np
import json

import requests
import settings

st.set_page_config(page_title = "Happy Coloring : User Page", page_icon="🏦")


def view(_id, _list, _chk):
    img_dict = []
    cap_dict = []
    nid_dict = []
    pic_dict = []
    nc = len(_list)
    row1 = st.columns(5)
    row2 = st.columns(5)
    if nc == 0 :
        return

    if _chk :
        if 'favorites' not in st.session_state:
            st.session_state['favorites'] = None

        if st.button("Add Favorites") :
            #st.write(st.session_state)
            if st.session_state['favorites'] is not None :
                for k, v in st.session_state['favorites'].items() :
                    myobj = {'user': int(v), 'picture' : int(k) }
                    #st.write(myobj)
                    r = requests.post(settings.commnad_dict['favorite'], json=myobj)
                    if r.status_code == 200 :
                        view(_id, r.json(), True)
                    else:
                        st.write(r.text)

                st.session_state['favorites'].clear()
                st.session_state['favorites'] = None

    for v in _list:
        path = "../images/" + str(v['author']).zfill(10)
        pid = v['id']
        nid = str(pid).zfill(10)
        of = path + "/" + nid + "_o.jpg"
        gf = path + "/" + nid + "_g.jpg"
        cf = path + "/" + nid + "_c.jpg"
        img_dict.append(cf)
        cap_dict.append(v['title'])
        nid_dict.append(nid)
        pic_dict.append(pid)
    #img = image_select(label="My Picture", images=img_dict, captions=cap_dict)
    index = 0
    for col in row1 + row2:
        tile = col.container(height=250, border=True)
        with tile:
            if _chk :
                val = st.checkbox(cap_dict[index])
                if val :
                    #st.write(cap_dict[index] + ' checked')
                    if st.session_state['favorites'] is None :
                        temp = { pic_dict[index] : _id }
                        st.session_state['favorites'] = temp
                    else:
                        if not pic_dict[index] in st.session_state['favorites']:
                            temp = { pic_dict[index] : _id }
                            st.session_state['favorites'] = st.session_state['favorites'] | temp
                else:
                    if st.session_state['favorites'] is not None :
                        if pic_dict[index] in st.session_state['favorites']:
                            del st.session_state['favorites'][pic_dict[index]]
            else:
                st.write(cap_dict[index])
            st.image(img_dict[index])
            po = st.popover("Details")
            with po :
                if st.button("Print", key=nid_dict[index]) :
                    myobj = {'user': _id, 'picture' : int(pic_dict[index]), 'printer' : st.session_state['user']['printer'], 'result' : '' }
                    r = requests.post(settings.commnad_dict['print'], json=myobj)
                    if r.status_code != 200 :
                        st.write(r.text)

                st.image(path + "/" + nid_dict[index] + "_o.jpg", width=300)
                st.image(path + "/" + nid_dict[index] + "_g.jpg", width=300)
        index = index + 1
        if index == nc :
            break



def Management():
    st.title(st.session_state['user']['nick'] + "'s Favorite")
    if st.session_state['user'] is not None :
        _id = st.session_state['user']['id']
        #st.write(_id)
        myobj = {'id': _id }
        r = requests.get(settings.commnad_dict['favorites'], json=myobj)
        #st.write(r.json())
        if r.status_code == 200 :
            view(_id, r.json(), False)
        else:
            st.write(r.text)

def PictureSearch():
    st.title("Picture Search")
    if st.session_state['user'] is not None :
        _id = st.session_state['user']['id']
        #st.write(_id)
        myobj = {'id': 0 }
        r = requests.get(settings.commnad_dict['pictures'], json=myobj)
        if r.status_code == 200 :
            view(_id, r.json(), True)
        else:
            st.write(r.text)

def PrintStat():
    st.title("Print Log")
    _id = st.session_state['user']['id']
    myobj = {'id': _id }
    r = requests.get(settings.commnad_dict['logs'], json=myobj)
    _jlist = r.json()

    df = pd.DataFrame(data=_jlist)
    st.dataframe(df)

def ChangeProfile():
    st.title("Log out")

def SetProfile():
    st.title("Change Profile")

def InitialPage():
    #st.sidebar.title('Author')
    #st.sidebar.title('Author')
    if 'user' not in st.session_state:
        myobj = {'email': 'user1@example.com'}
        r = requests.get(settings.commnad_dict['user'], json=myobj)
        st.session_state['user'] = r.json()
        id = st.session_state['user']['id']
        path = str.format("../images/%s" % str(id).zfill(10))
        if not os.path.exists(path) :
            os.mkdir(path)

    pg = st.navigation({
        "User" : [st.Page(Management, title="Favorite"), st.Page(PictureSearch, title="Search"), st.Page(PrintStat, title="Log")],
        "Account" : [st.Page(ChangeProfile, title="Log out"), st.Page(SetProfile, title="Setting")]
    })

    pg.run()


def User():

    InitialPage()

User()
