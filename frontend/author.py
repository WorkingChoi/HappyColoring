import base64
import io
import os
from pathlib import Path

import numpy as np
import pandas as pd
from io import StringIO

from PIL import Image

import streamlit as st
from streamlit_image_select import image_select

import requests
import settings

st.set_page_config(page_title = "Happy Coloring : Author Page", page_icon="🏦")

@st.cache_data
def _encode_file(img):
    with open(img, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/jpeg;base64, {encoded}"

@st.cache_data
def _encode_numpy(img):
    pil_img = Image.fromarray(img)
    buffer = io.BytesIO()
    pil_img.save(buffer, format="JPEG")
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/jpeg;base64, {encoded}"

def view(_id, _list):
    img_dict = []
    cap_dict = []
    nid_dict = []
    nc = len(_list)
    row1 = st.columns(5)
    row2 = st.columns(5)

    path = "../images/" + str(_id).zfill(10)
    for v in _list:
        nid = str(v['id']).zfill(10)
        of = path + "/" + nid + "_o.jpg"
        gf = path + "/" + nid + "_g.jpg"
        cf = path + "/" + nid + "_c.jpg"
        img_dict.append(cf)
        cap_dict.append(v['title'])
        nid_dict.append(nid)
    #img = image_select(label="My Picture", images=img_dict, captions=cap_dict)
    index = 0
    for col in row1 + row2:
        tile = col.container(height=240, border=True)
        with tile:
            st.write(cap_dict[index])
            st.image(img_dict[index])
            po = st.popover("Details")
            with po :
                if st.button("Print", key=nid_dict[index]) :
                    myobj = {'user': _id, 'picture' : int(nid_dict[index]), 'print' : '', 'result' : '' }
                    r = requests.post(settings.commnad_dict['print'], json=myobj)
                    if r.status_code != 200 :
                        st.write(r.text)

                st.image(path + "/" + nid_dict[index] + "_o.jpg", width=300)
                st.image(path + "/" + nid_dict[index] + "_g.jpg", width=300)
        index = index + 1
        if index == nc :
            break

def Management():
    st.title(st.session_state['user']['nick'])
    if st.session_state['user'] is not None :
        _id = st.session_state['user']['id']
        #st.write(_id)
        myobj = {'id': _id }
        r = requests.get(settings.commnad_dict['pictures'], json=myobj)
        if r.status_code == 200 :
            view(_id, r.json())
        else:
            st.write(r.text)


def NewPicture():
    st.title("Enroll Picture")
    if 'enroll_o' not in st.session_state:
        st.session_state['enroll_o'] = None
    if 'enroll_g' not in st.session_state:
        st.session_state['enroll_g'] = None
    if 'enroll_c' not in st.session_state:
        st.session_state['enroll_c'] = None
    title = st.text_input("Title : ", key="title")
    if st.button("Submit"):
        if st.session_state['enroll_o'] == None or 'enroll_o' not in st.session_state :
            st.write("Please Set Out Line Image")
        elif st.session_state['enroll_g'] == None or 'enroll_g' not in st.session_state :
            st.write("Please Set Guide Image")
        elif st.session_state['enroll_c'] == None or 'enroll_c' not in st.session_state :
            st.write("Please Set Origin Image")
        elif len(title) == 0 :
            st.write("Please Set Title")
        else :
            _id = st.session_state['user']['id']
            myobj = {'author': _id, 'title' : title }
            r = requests.post(settings.commnad_dict['enroll'], json=myobj)
            if r.status_code == 200 :
                st.write("Enroll Success : " + title + ", " + str(r.status_code))
                st.write(st.session_state['enroll_o'])
                st.write(st.session_state['enroll_g'])
                st.write(st.session_state['enroll_c'])
                st.session_state['enroll_o'] = None
                st.session_state['enroll_g'] = None
                st.session_state['enroll_c'] = None
                title = ""
            else :
                st.write("Enroll Fail : " + title + ", " + str(r.status_code))


    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Out Line")
        uploaded_file = st.file_uploader("Choose a JPG file", accept_multiple_files=False, type="jpg", key="out")

        if uploaded_file is not None:
            bytes_data = uploaded_file.read()
            id = st.session_state['user']['id']
            path = str.format("../images/%s" % str(id).zfill(10))
            if not os.path.exists(path) :
                os.mkdir(path)
            fname = path + "/outline.jpg"
            with open(fname, "wb") as f:
                f.write(bytes_data)
            st.write("filename:", uploaded_file.name)
            st.image(fname)
            st.session_state['enroll_o'] = fname

    with col2:
        st.header("Guide")
        uploaded_file2 = st.file_uploader("Choose a JPG file", accept_multiple_files=False, type="jpg", key="guide")

        if uploaded_file2 is not None:
            bytes_data = uploaded_file2.read()
            id = st.session_state['user']['id']
            path = str.format("../images/%s" % str(id).zfill(10))
            if not os.path.exists(path) :
                os.mkdir(path)
            fname2 = path + "/guide.jpg"
            with open(fname2, "wb") as f:
                f.write(bytes_data)
            st.write("filename:", uploaded_file2.name)
            st.image(fname2)
            st.session_state['enroll_g'] = fname2

    with col3:
        st.header("Origin")
        uploaded_file3 = st.file_uploader("Choose a JPG file", accept_multiple_files=False, type="jpg", key="color")

        if uploaded_file3 is not None:
            bytes_data = uploaded_file3.read()
            id = st.session_state['user']['id']
            path = str.format("../images/%s" % str(id).zfill(10))
            if not os.path.exists(path) :
                os.mkdir(path)
            fname3 = path + "/color.jpg"
            with open(fname3, "wb") as f:
                f.write(bytes_data)
            st.write("filename:", uploaded_file3.name)
            st.image(fname3)
            st.session_state['enroll_c'] = fname3

def PrintStat():
    st.title("Print Log")
    if st.session_state['user'] is not None :
        _id = st.session_state['user']['id']
        myobj = {'id': _id }
        r = requests.get(settings.commnad_dict['logs'], json=myobj)
        if r.status_code == 200 :
            _jlist = r.json()

            df = pd.DataFrame(data=_jlist)
            st.dataframe(df)
        else:
            st.write(r.text)

def ChangeProfile():
    st.title("Log out")

def SetProfile():
    st.title("ChangeProfile")

def TestPage():
    st.title("Test")
    st.write(st.session_state)

def InitialPage():
    #st.sidebar.title('Author')
    if 'user' not in st.session_state:
        myobj = {'email': 'author@example.com'}
        r = requests.get(settings.commnad_dict['user'], json=myobj)
        st.session_state['user'] = r.json()
        id = st.session_state['user']['id']
        path = str.format("../images/%s" % str(id).zfill(10))
        if not os.path.exists(path) :
            os.mkdir(path)

    pg = st.navigation({
        #"Author" : [st.Page(TestPage, title="Test"), st.Page(Management, title="Picture"), st.Page(NewPicture, title="New"), st.Page(PrintStat, title="Manage")],
        "Author" : [st.Page(Management, title="Picture"), st.Page(NewPicture, title="New"), st.Page(PrintStat, title="Manage")],
        "Account" : [st.Page(ChangeProfile, title="Log out"), st.Page(SetProfile, title="Setting")]
    })

    pg.run()


def Author():

    InitialPage()



Author()
