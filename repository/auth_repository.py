from common.mongo import mongodb
import logging, os
from typing import List
from botocore.exceptions import ClientError
from fastapi import HTTPException
from starlette import status
from fastapi.encoders import jsonable_encoder

from dotenv import load_dotenv
load_dotenv()
COL_USER = os.getenv('COL_USER')
COL_PERMISION = os.getenv('COL_PERMISION')
COL_ROLE = os.getenv('COL_ROLE')
COL_LOCATION = os.getenv('COL_LOCATION')
COL_PROVINE = os.getenv('COL_PROVINE')
COL_WARD = os.getenv('COL_WARD')
COL_DISTRICT = os.getenv('COL_DISTRICT')
COL_QUARTER = os.getenv('COL_QUARTER')
COL_STATIONS = os.getenv('COL_STATIONS')
COL_NODE_REGISTRY = os.getenv('COL_NODE_REGISTRY')
COL_FILES = os.getenv('COL_FILES')

async def get_role_info_by_userid(userid: str):
    logging.info("===>>> auth_repository.py <<<===")
    logging.info("===>>> get_role_info_by_userid <<<===")
    try:
        out = []
        userid_query = { "userid": str(userid)}
        obj_mongo = mongodb()
        obj_mongo.col(COL_ROLE)
        for each in obj_mongo.mycol.find(userid_query):
            each['_id'] = str(each.get("_id"))
            out.append(each)
        obj_mongo.closedb()
        return out
    except ClientError as e:
        logging.info("===>>> Error <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)

async def get_user_by_email(email):
    logging.info("===>>> auth_repository.py <<<===")
    logging.info("===>>> get_user_by_email <<<===")
    try:
        out = []
        email_query = { "email": str(email)}
        obj_mongo = mongodb()
        obj_mongo.col(COL_USER)
        for each in obj_mongo.mycol.find(email_query):
            each['_id'] = str(each.get("_id"))
            out.append(each)
        obj_mongo.closedb()
        return out
    except ClientError as e:
        logging.info("===>>> Error <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)

async def add_user(user):
    logging.info("===>>> auth_repository.py <<<===")
    logging.info("===>>> add_user <<<===")
    try:
        obj_mongo = mongodb()
        obj_mongo.col(COL_USER)
        user = obj_mongo.mycol.insert_one(user)
        obj_mongo.closedb()
        return user.get('userid')
    except ClientError as e:
        logging.info("===>>> Error <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)

async def get_token_by_refresh_token(refresh_token):
    logging.info("===>>> auth_repository.py <<<===")
    logging.info("===>>> get_token_by_refresh_token <<<===")
    try:
        out = []
        refresh_token_query = { "refresh_token": str(refresh_token)}
        obj_mongo = mongodb()
        obj_mongo.col(COL_USER)
        for each in obj_mongo.mycol.find(refresh_token_query):
            each['_id'] = str(each.get("_id"))
            out.append(each)
        obj_mongo.closedb()
        return out
    except ClientError as e:
        logging.info("===>>> Error <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)

async def get_token_by_userid(userid: str):
    logging.info("===>>> auth_repository.py <<<===")
    logging.info("===>>> get_token_by_userid <<<===")
    try:
        out = []
        userid_token_query = { "userid": str(userid)}
        obj_mongo = mongodb()
        obj_mongo.col(COL_USER)
        for each in obj_mongo.mycol.find(userid_token_query):
            each['_id'] = str(each.get("_id"))
            out.append(each)
        obj_mongo.closedb()
        return out
    except ClientError as e:
        logging.info("===>>> Error <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)

async def update_refresh_token_by_userid(userid, new_refresh_token):
    logging.info("===>>> auth_repository.py <<<===")
    logging.info("===>>> update_token_by_userid <<<===")
    try:
        userid_token_update = { "userid": str(userid)}
        obj_mongo = mongodb()
        obj_mongo.col(COL_USER)
        data = obj_mongo.mycol.update_one(userid_token_update, { "$set": { 'refresh_token': new_refresh_token } })
        obj_mongo.closedb()
        return data
    except ClientError as e:
        logging.info("===>>> Error <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)

async def update_token_by_userid(userid, new_token):
    logging.info("===>>> auth_repository.py <<<===")
    logging.info("===>>> update_token_by_userid <<<===")
    try:
        userid_token_update = { "userid": str(userid)}
        obj_mongo = mongodb()
        obj_mongo.col(COL_USER)
        data = obj_mongo.mycol.update_one(userid_token_update, { "$set": { 'token': new_token } })
        obj_mongo.closedb()
        return data
    except ClientError as e:
        logging.info("===>>> Error <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


async def update_last_login_by_userid(userid, last_login):
    logging.info("===>>> auth_repository.py <<<===")
    logging.info("===>>> update_last_login_by_userid <<<===")
    try:
        userid_last_login_update = { "userid": str(userid)}
        obj_mongo = mongodb()
        obj_mongo.col(COL_USER)
        data = obj_mongo.mycol.update_one(userid_last_login_update, { "$set": { 'last_login': last_login } })
        obj_mongo.closedb()
        return data
    except ClientError as e:
        logging.info("===>>> Error <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


