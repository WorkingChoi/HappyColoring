from sqlalchemy import Column, Integer, String, Text, DateTime, sql, ForeignKey
from sqlalchemy.dialects import postgresql
from database import Base

class UserTBL(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    nick = Column(String, nullable=False)
    name = Column(String, nullable=False)
    roll = Column(String, nullable=False, default="user")
    grade = Column(String, nullable=True)
    year = Column(String, nullable=True)
    pw = Column(String, nullable=False)
    printer = Column(String)
    comment = Column(Text)
    enroll_time = Column(DateTime(timezone=True), server_default=sql.func.now())
    use_yn = Column(String, default='Y')

class PictureTBL(Base):
    __tablename__ = "picture"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)
    enroll_time = Column(DateTime(timezone=True), server_default=sql.func.now())
    use_yn = Column(String, default='Y')

class FavoriteTBL(Base):
    __tablename__ = "favorite"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("user.id"))
    picture = Column(Integer, ForeignKey("picture.id"))
    enroll_time = Column(DateTime(timezone=True), server_default=sql.func.now())
    use_yn = Column(String, default='Y')

class ConsumeTBL(Base):
    __tablename__ = "consume"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("user.id"))
    picture = Column(Integer, ForeignKey("picture.id"))
    base = Column(String, nullable=False)
    count = Column(Integer, default=0)


class PrintLogTBL(Base):
    __tablename__ = "print_log"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey("user.id"))
    picture = Column(Integer, ForeignKey("picture.id"))
    printer = Column(String)
    result = Column(Text)
    log_time = Column(DateTime(timezone=True), server_default=sql.func.now())

