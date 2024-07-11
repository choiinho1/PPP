from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

import uvicorn
from domain.event import event_router
from domain.user import user_router

app = FastAPI()

app.include_router(event_router.router) #include_router 메소드 -> 라우터 등록
app.include_router(user_router.router)