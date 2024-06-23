import datetime

from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo

class User(BaseModel):
    id: int
    email: str
    nick: str
    name: str
    roll: str
    printer: str
    enroll_time: datetime.datetime

class UserID(BaseModel):
    id: int

class UserEmail(BaseModel):
    email: str

class UserCreate(BaseModel):
    name: str
    nick: str
    pw1: str
    pw2: str
    email: EmailStr

    @field_validator('nick', 'name', 'pw1', 'pw2', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @field_validator('pw2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'pw1' in info.data and v != info.data['pw1']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v

class Picture(BaseModel):
    id: int
    title: str
    author: int
    enroll_time: datetime.datetime

class PictureID(BaseModel):
    id: int

class PictureCreate(BaseModel):
    title: str
    author: int

class Consume(BaseModel):
    id: int
    user: int
    picture: int
    base: str
    count: int

class Favorite(BaseModel):
    id: int
    user: int
    picture: int

class FavoriteCreate(BaseModel):
    user: int
    picture: int

class PrintLog(BaseModel):
    id: int
    user: int
    picture: int
    printer: str
    log_time: datetime.datetime

class PrintLogCreate(BaseModel):
    user: int
    picture: int
    printer: str
    result: str

class PrintLogID(BaseModel):
    user: int
    picture: int
