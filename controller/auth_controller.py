import logging
from botocore.exceptions import ClientError
from fastapi import APIRouter, Response
from starlette import status
from starlette.exceptions import HTTPException
from config.route import Route
from models import schemas
from service import auth_service

router = APIRouter()

@router.post(Route.V1.REGISTER)
async def register(user_create: schemas.Register):
    logging.info("===>>> auth_controller.py <<<===")
    logging.info("===>>> function register <<<===")
    try:
        return await auth_service.register(user_create)
    except ClientError or Exception as e:
        logging.info("===>>> Error <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


@router.post(Route.V1.LOGIN)
async def login(user: schemas.LogIn, response: Response):
    logging.info("===>>> auth_controller.py <<<===")
    logging.info("===>>> function login <<<===")
    try:
        return await auth_service.login(user=user, response = response)
    except ClientError or Exception as e:
        logging.info("===>>> Error <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)

@router.post(Route.V1.REFRESH_TOKEN)
async def refresh_token(refresh_token: schemas.RefreshToken, response: Response):
    logging.info("===>>> auth_controller.py <<<===")
    logging.info("===>>> function refresh_token <<<===")
    try:
        return await auth_service.refresh_token(refresh_token, response = response)
    except ClientError or Exception as e:
        logging.info("===>>> Error <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)

@router.post(Route.V1.LOGOUT)
async def logout(refresh_token: schemas.RefreshToken):
    logging.info("===>>> auth_controller.py <<<===")
    logging.info("===>>> function logout <<<===")
    try:
        return await auth_service.logout(refresh_token)
    except ClientError or Exception as e:
        logging.info("===>>> Error <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)
