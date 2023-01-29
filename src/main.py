import logging
from logging.config import dictConfig

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1.file_storage import storage_router
from src.api.v1.ping import ping_router
from src.core.config import app_settings
from src.core.logger import LOGGING
from src.schemas.user import UserRead, UserCreate, UserUpdate
from src.services.user_manager import fastapi_users_router, auth_backend

dictConfig(LOGGING)
logger = logging.getLogger('root')


app = FastAPI(
    title=app_settings.APP_TITLE,
    default_response_class=ORJSONResponse,
)

app.include_router(
    fastapi_users_router.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users_router.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users_router.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users_router.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users_router.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(storage_router)
app.include_router(ping_router)

if __name__ == '__main__':
    logger.info('Server started')
    uvicorn.run(
        'main:app',
        host=app_settings.HOST,
        port=app_settings.PORT,
    )
