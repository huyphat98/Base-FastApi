from hashlib import new
import json
import jwt, os
from datetime import datetime, timedelta
from fastapi import HTTPException
from pydantic import ValidationError
from models.schemas import SetTimeOutToken
from repository import auth_repository

from dotenv import load_dotenv
load_dotenv()

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY_TOKEN = os.getenv('SECRET_KEY_TOKEN')
SECRET_KEY_REFRESH_TOKEN = os.getenv('SECRET_KEY_REFRESH_TOKEN')

###################################################################################
###### Generate Token
###################################################################################
async def generate_token(userid: str, location_id: str) -> str:
    seconds = SetTimeOutToken.seconds
    expire = datetime.now() + timedelta(seconds=seconds)
    to_encode = {
        "exp": expire.timestamp(),
        'userid': userid,
        'location_id': location_id
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_TOKEN, algorithm=SECURITY_ALGORITHM)
     # update token on DB
    await auth_repository.update_token_by_userid(userid, str(encoded_jwt.decode()))
    return encoded_jwt

###################################################################################
###### Validate Token
###################################################################################
async def validate_token(access_token) -> json:
    """
    Decode JWT token to get username => return payload

    """
    try:
        if access_token:
            access_token = access_token.replace('Bearer ', '')
            payload = jwt.decode(access_token, SECRET_KEY_TOKEN, algorithms=[SECURITY_ALGORITHM])
            if payload.get('exp') < datetime.now().timestamp():
                raise HTTPException(status_code=403, detail="Token expired")
            payload['access_token'] = access_token
            return payload
        else:
            raise HTTPException(status_code=401, detail="Access Denied")
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )

###################################################################################
###### Generate RefreshToken
###################################################################################
async def generate_refresh_token(userid: str, location_id: str) -> str:
    seconds = SetTimeOutToken.seconds_day * SetTimeOutToken.day  # Expired after 1 days
    expire = datetime.now() + timedelta(seconds=seconds)

    to_encode = {
        "exp": expire.timestamp(),
        'userid': userid,
        'location_id': location_id
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_REFRESH_TOKEN, algorithm=SECURITY_ALGORITHM)

    # update refresh token on DB
    await auth_repository.update_refresh_token_by_userid(userid, str(encoded_jwt.decode()))
    return encoded_jwt

###################################################################################
###### Validate RefreshToken
###################################################################################
async def validate_refresh_token(refresh_token)-> json:
    """
    Decode JWT refresh_token to get username => return payload

    """
    try:
        if refresh_token:
            refresh_token = refresh_token.replace('Bearer ', '')
            payload = jwt.decode(refresh_token, SECRET_KEY_REFRESH_TOKEN, algorithms=[SECURITY_ALGORITHM])
            if payload.get('exp') < datetime.now().timestamp():
                raise HTTPException(status_code=403, detail="RefreshToken expired")
            payload['refresh_token'] = refresh_token
            return payload
        else:
            raise HTTPException(status_code=401, detail="Access Denied")
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )
