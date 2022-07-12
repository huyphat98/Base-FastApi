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

async def get_stations(station_id: str):
    logging.info("===>>> station_service.py <<<===")
    logging.info("===>>> function get_stations <<<===")
    try:
        return {'code': 200}
    except ClientError as e:
        logging.info("===>>> Error <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)