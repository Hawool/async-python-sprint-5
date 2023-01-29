import shutil

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import app_settings
from src.db.db import get_session
from src.models.user import User
from src.schemas.file import FileCreate
from src.services.file import file_crud
from src.services.user_manager import current_active_user

storage_router = APIRouter(prefix='/storage', tags=['File storage'])


@storage_router.post('', status_code=201, response_model=FileCreate)
async def save_file(
        file: UploadFile,
        name: str,
        db: AsyncSession = Depends(get_session),
        user: User = Depends(current_active_user)
) -> FileCreate:
    file_path = f'{app_settings.FILE_FOLDER}{file.filename}'
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    obj_in = FileCreate(path=file_path, name=name, user_id=user.id)
    await file_crud.create(db=db, obj_in=obj_in)
    return obj_in
