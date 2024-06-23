import streamlit as st

host = "http://localhost:8000/"
commnad_dict = {
    "user" : host + "api/user",
    "users" : host + "api/users",
    "pictures" : host + "api/pictures",
    "picture" : host + "api/picture",
    "print" : host + "api/print",
    "logs" : host + "api/logs",
    "enroll" : host + "api/enroll",
    "favorite" : host + "api/favorite",
    "favorites" : host + "api/favorites"
}
