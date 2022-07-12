import logging
import os, json, time
import re
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi import FastAPI, Request
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import asyncio
from config.route import Route
from controller import auth_controller, station_controller
from log.log import Log
from botocore.exceptions import ClientError
from security import jwt_authen
from repository import auth_repository
from starlette import status
from classlib.classLocate import LocationManager
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

######## MIDDLEWARE AUTH
@app.middleware("http")
async def middleware_authenticate(request: Request, call_next):
    try:
        loc = LocationManager(debug = 1)
        start_time = time.time()
        logging.info("========================== REQUEST ==========================")
        token_header = request.headers.get('x-authorization')
        response = await call_next(request)
        if request.url.path.startswith(Route.V1.prefix_api + Route.V1.LOGIN) \
                or request.url.path.startswith('/docs') \
                or request.url.path.startswith('/favicon.ico') \
                or request.url.path.startswith('/openapi.json'):
            return response

        if token_header is not None and str(token_header).startswith('Bearer '):
            access_token = token_header.replace('Bearer ', '')
            # handle
            ## check exp time token, validate token -> userid and location_id
            token_data_obj = await jwt_authen.validate_token(access_token)

            ## check userid
            user_db = await auth_repository.get_token_by_userid(token_data_obj.get('userid'))
            if len(user_db) == 0:
                return Response(
                    content=b"user is not found!",
                    status_code=status.HTTP_404_NOT_FOUND
                )
            ## get location from location_id
            location_info = loc.GetLocInfo(location_id=str(token_data_obj.get('location_id')))
            print(location_info)

            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return response
        else:
            return Response(
                content=b"X-Token header invalid",
                status_code=status.HTTP_403_FORBIDDEN
            )
    except ClientError as e:
        raise HTTPException(status_code=401, detail="X-Token header invalid")


app.include_router(auth_controller.router, prefix=Route.V1.prefix_api, tags=['Auth'],
                   responses={404: {"description": "Not found"}})
app.include_router(station_controller.router, prefix=Route.V1.prefix_api, tags=['Station'],
                   responses={404: {"description": "Not found"}})

def custom_openapi():
    """
    Custom information docs openapi in link : http://{domain}/docs
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=os.getenv('OPENAPI_TITLE'),
        version=os.getenv('OPENAPI_VERSION'),
        description=os.getenv('OPENAPI_DESCRIPTION'),
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    # =================== LOG FILE
    logger = Log()
    uvicorn.run(app='main_authen:app', host="0.0.0.0", port=46000, reload=True, log_level="debug")
