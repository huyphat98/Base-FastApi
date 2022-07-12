import logging
from botocore.exceptions import ClientError
from fastapi import APIRouter, Response
from starlette import status
from starlette.exceptions import HTTPException
from config.route import Route
from models import schemas
from service import auth_service, station_service

router = APIRouter()

@router.get(Route.V1.GETSTATION)
async def get_station(station_id: str):
    logging.info("===>>> station_controller.py <<<===")
    logging.info("===>>> function get_station <<<===")
    try:
        return await station_service.get_stations(station_id)
    except ClientError or Exception as e:
        logging.info("===>>> Error <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)