from typing import List
from pydantic import BaseModel

class SetTimeOutToken:
    seconds_day = 86400 # 1 ngày
    day = 1
    seconds = 15 # 15s

class LogIn(BaseModel):
    email: str = None
    password: str = None

class RefreshToken(BaseModel):
    refresh_token: str = None

class Register(BaseModel):
    email: str = None
    username: str = None
    password: str = None




