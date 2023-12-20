from http import HTTPStatus
from fastapi import APIRouter, Depends, Response
from typing import Dict
from src.auth import utils
from src.auth.models import user_req, user_req
from src.auth.service import insert_user, validate_creds
from src.database import database

auth_router = APIRouter(prefix="/auth")

@auth_router.post(path="/login", status_code=HTTPStatus.OK)
async def login(
    body: user_req,
    resp: Response,
    conn=Depends(database.get_conn)
) -> Dict[str, str]:
    token = await validate_creds(body, conn)
    utils.set_access_token(resp, token)
    return {"message": "User logged in"}

@auth_router.post(path="/register", status_code=HTTPStatus.CREATED)
async def register(
    body: user_req,
    resp: Response,
    conn=Depends(database.get_conn)
) -> Dict[str, str]:
    token = await insert_user(body, conn)
    utils.set_access_token(resp, token)
    return {"message": "User created"}
