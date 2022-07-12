import logging
import os, datetime
import re, uuid
from botocore.exceptions import ClientError
from fastapi import HTTPException, Response
from starlette import status
from typing import List
from models import schemas
from common import validate, stype_prefix
from repository import auth_repository
from security import jwt_authen

async def login(user: schemas.LogIn, response: Response):
    logging.info("===>>> auth_service.py <<<===")
    logging.info("===>>> function login <<<===")
    try:
        if user.password is None or user.email is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='email and password is not none')
        # LETS VALIDATE THE DATA BEFORE WE A USER
        check_data = await validate.check_validate_login(user.email, user.password)
        if check_data==False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='validation data false')

        # Checking if the email exist
        user_db = await auth_repository.get_user_by_email(user.email)
        if len(user_db) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='email is wrong!')

        # get location information
        role_info = await auth_repository.get_role_info_by_userid(str(user_db[0]['userid']))

        # PASSWORD IS CORRECT
        hashedPassword = await validate.hash_password(user.password)
        if hashedPassword != user_db[0]['secret']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid password')

        # Create and assign a token
        if role_info:
            # generate and update token on DB
            accessToken = await jwt_authen.generate_token(str(user_db[0]['userid']), role_info[0]['location_id'])
            refreshToken = await jwt_authen.generate_refresh_token(str(user_db[0]['userid']), role_info[0]['location_id'])

            # update last_login
            last_login = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            auth_repository.update_last_login_by_userid(str(user_db[0]['userid']), last_login)
            return {
                'code': 200,
                'msg': {
                    'accessToken': accessToken,
                    'refreshToken': refreshToken,
                    'last_login': last_login
                }
            }
        return {'code': 404}
    except ClientError as e:
        logging.info("===>>> Error <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


async def refresh_token(refresh_token: schemas.RefreshToken, response: Response):
    logging.info("===>>> auth_service.py <<<===")
    logging.info("===>>> function refresh_token <<<===")
    try:
        if refresh_token.refresh_token is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='is not refreshToken')
        # get user by refresh token
        token_db = await auth_repository.get_token_by_refresh_token(refresh_token.refresh_token)
        if len(token_db) == 0:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='refreshToken already exists')

        # check expire refresh token
        await jwt_authen.validate_refresh_token(refresh_token.refresh_token)

        # generate access token
        userid = token_db[0]['userid']
        accessToken = await jwt_authen.generate_token(userid)

        return {
            'code': 200,
            'msg': {
                'accessToken': accessToken
            }
        }
    except ClientError as e:
        logging.info("===>>> Error <<<===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)

async def logout(refresh_token: schemas.RefreshToken):
    logging.info("===>>> auth_service.py <<<===")
    logging.info("===>>> function logout <<<===")
    try:
        if refresh_token.refresh_token is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='is not refreshToken')

        # check expire refresh token
        data_refresh_token = await jwt_authen.validate_refresh_token(refresh_token.refresh_token)

        # check user
        user_db = await auth_repository.get_token_by_userid(data_refresh_token['userid'])
        if len(user_db) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user is not found!')

        # update refresh token
        await auth_repository.update_refresh_token_by_userid(data_refresh_token['userid'], '')

        # update token token
        await auth_repository.update_token_by_userid(data_refresh_token['userid'], '')

        return {
            'code': 200,
            'msg': 'success'
        }
    except ClientError as e:
        logging.info("===>>> Error <<<===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)

async def register(create_user: schemas.Register):
    logging.info("===>>> auth_service.py <<<===")
    logging.info("===>>> function register <<<===")
    try:
        if create_user.password is None or create_user.username is None or create_user.email is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='email, username and password is not none')
        # LETS VALIDATE THE DATA BEFORE WE A USER
        check_data = await validate.check_validate_register(create_user.username, create_user.password, create_user.email)
        if check_data==False:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='validation data false')
        # Checking if the user is already in the database
        user_db = await auth_repository.get_user_by_email(create_user.email)
        if len(user_db) != 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='email already exists')
        # Hash passwords
        hashedPassword = await validate.hash_password(create_user.password)

        # Add user
        user = {
            'mail': create_user.email,
            'username': create_user.username,
            'secret': hashedPassword,
            'desc': None,
            'userid': str(uuid.uuid4()),
            'regex_username': None,
            'alarmlisten': None,
            'token': None,
            'refresh_token': None,
            'last_login': None
        }
        userid = await auth_repository.add_user(user)
        if userid is not None:
            return {
                'code': 200,
                'msg': {
                    'userid': userid
                }
            }
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')

    except ClientError as e:
        logging.info("===>>> Error <<<===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)