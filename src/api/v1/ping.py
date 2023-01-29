import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_session

ping_router = APIRouter(prefix='/ping', tags=['Ping'])


@ping_router.get('/all', status_code=200)
async def ping(db: AsyncSession = Depends(get_session)):
    statement = text("""SELECT 1""")
    start = datetime.datetime.now()
    await db.execute(statement)
    return {'db': datetime.datetime.now() - start}
