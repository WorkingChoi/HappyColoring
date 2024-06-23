from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import get_db

import os
import time

import models
import schema
import epson

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {
        "message": "Hello Jamppo's FastAPI"
    }

'''
user list
'''
@app.get("/api/users", response_model=list[schema.User])
async def user_list(db: Session = Depends(get_db)) :
    _user_list = db.query(models.UserTBL).order_by(models.UserTBL.enroll_time.desc()).all()
    return _user_list

'''
Add User
'''
@app.post("/api/user")
async def add_user(_user_create: schema.UserCreate, db: Session = Depends(get_db)) :
    #print(_user_create.nick, _user_create.name, _user_create.email)
    db_user = models.UserTBL(name=_user_create.name,
                      nick=_user_create.nick,
                   pw=pwd_context.hash(_user_create.pw1),
                   email=_user_create.email)
    db.add(db_user)
    db.commit()
    return _user_create

'''
Get User
'''
@app.get("/api/user")
async def get_user(_id: schema.UserEmail, db: Session = Depends(get_db)) :
    print(_id.email)
    _user = db.query(models.UserTBL).filter(models.UserTBL.email==_id.email).first()
    print(_user)
    return _user

'''
Picture List
'''
@app.get("/api/pictures", response_model=list[schema.Picture])
async def picture_list(_id: schema.UserID, db: Session = Depends(get_db)) :
    #print("picture_list")
    #print(_id.id)
    if _id.id == 0 :
        _list = db.query(models.PictureTBL).order_by(models.PictureTBL.enroll_time.desc()).all()
    else :
        _list = db.query(models.PictureTBL).order_by(models.PictureTBL.enroll_time.desc()).filter(models.PictureTBL.author ==_id.id).all()
    return _list

'''
Get Picture
'''
@app.get("/api/picture")
async def get_pic(_id: schema.PictureID, db: Session = Depends(get_db)) :
    _pic = db.query(models.PictureTBL).get(_id.id)
    return _pic

'''
Delete Picture
'''
@app.delete("/api/picture")
async def del_pic(_id: schema.PictureID, db: Session = Depends(get_db)) :
    _pic = db.query(models.PictureTBL).get(_id.id)
    db.delete(_pic)
    db.commit()
    return _pic

'''
Add Favorite
'''
@app.post("/api/favorite")
async def add_fav(_fav: schema.FavoriteCreate, db: Session = Depends(get_db)) :
    print(_fav)
    _f = models.FavoriteTBL(user=int(_fav.user), picture=int(_fav.picture))
    print(_f)
    db.add(_f)
    db.commit()
    return _f

'''
Get Favorite List
'''
@app.get("/api/favorites", response_model=list[schema.Picture])
async def fav_list(_id: schema.UserID, db: Session = Depends(get_db)) :
    _list = db.query(models.PictureTBL).order_by(models.FavoriteTBL.enroll_time.desc()).filter(models.PictureTBL.id == models.FavoriteTBL.picture).filter(models.FavoriteTBL.user ==_id.id).all()
    return _list


'''
Log List
'''
@app.get("/api/logs", response_model=list[schema.PrintLog])
async def log_list(_id: schema.UserID, db: Session = Depends(get_db)) :
    #print("log_list")
    #print(_id.id)
    if int(_id.id) == 0 :
        _list = db.query(models.PrintLogTBL).order_by(models.PrintLogTBL.log_time.desc()).all()
        return _list
    else :
        _list = db.query(models.PrintLogTBL).order_by(models.PrintLogTBL.log_time.desc()).filter(models.PrintLogTBL.user == int(_id.id)).all()
        return _list

def move_file(id, author):
    path = "../images/" + str(author).zfill(10)

    o_ofile = path + "/outline.jpg"
    o_gfile = path + "/guide.jpg"
    o_cfile = path + "/color.jpg"

    nid = str(id).zfill(10)

    n_ofile = path + "/" + nid + "_o.jpg"
    n_gfile = path + "/" + nid + "_g.jpg"
    n_cfile = path + "/" + nid + "_c.jpg"

    if os.path.exists(o_ofile) and os.path.exists(o_gfile) and os.path.exists(o_cfile) :
        os.rename(o_ofile, n_ofile)
        os.rename(o_gfile, n_gfile)
        os.rename(o_cfile, n_cfile)

'''
Enroll Picture
'''
@app.post("/api/enroll")
async def enroll_pic(_pic_create: schema.PictureCreate, db: Session = Depends(get_db)) :
    _pic = models.PictureTBL(title=_pic_create.title, author=_pic_create.author)
    db.add(_pic)
    db.commit()
    move_file(_pic.id, _pic.author)
    return _pic

'''
Print Picture
'''
@app.post("/api/print")
async def print_pic(_pic_log: schema.PrintLogCreate, db: Session = Depends(get_db)) :
    pid=_pic_log.picture
    print(pid)
    _pic = db.query(models.PictureTBL).get(pid)
    path = "../images/" + str(_pic.author).zfill(10)
    nid = str(pid).zfill(10)
    of = path + "/" + nid + "_o.jpg"
    print(of)
    ret = epson.epson_print(nid, _pic_log.printer, of)
    time.sleep(0.1)
    _pic_log.result = of + "=" + ret
    gf = path + "/" + nid + "_g.jpg"
    ret = epson.epson_print(nid, _pic_log.printer, gf)
    time.sleep(0.1)
    _pic_log.result = _pic_log.result + ", " + gf + "=" + ret
    cf = path + "/" + nid + "_c.jpg"
    ret = epson.epson_print(nid, _pic_log.printer, cf)
    _pic_log.result = _pic_log.result + ", " + cf + "=" + ret
    _log = models.PrintLogTBL(user=_pic_log.user, picture=_pic_log.picture, printer=_pic_log.printer, result=_pic_log.result)
    db.add(_log)
    db.commit()
    return _pic_log

