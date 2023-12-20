from asyncpg.connection import Connection
import bcrypt
from http import HTTPStatus
from fastapi import HTTPException
import jwt
import os
from src.auth.models import user_req, user_req, user, user_cred
from src.auth import repository as repo
from src.exceptions import ConflictError, InternalError, NotFoundError

async def validate_creds(usr: user_req, conn: Connection) -> str:
    """
    retrieve user credentials from database and validate password against hash

    Args:
        usr (user_req): model containing user email and password
        conn (Connection): database connection

    Raises:
        HTTPException: Unauthorized if password is invalid
        HTTPException: NotFoundError if user does not exist
        HTTPException: InternalServerError if database query fails

    Returns:
        str: JWT token
    """
    try:
        # fetch user credentials from database
        usr_creds: user_cred = await repo.get_user_cred(usr.email, conn)
        
        # validate password
        if not bcrypt.checkpw(usr.password.encode('utf-8'), usr_creds.password):
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid credentials")
        
        # return JWT token
        return jwt.encode(
            payload={"user_id": str(usr_creds.user_id), "role": usr_creds.role},
            key=os.environ.get("JWT_SECRET"),
        )
    except NotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=e.msg)
    except InternalError as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=e.msg)

async def insert_user(usr: user_req, conn: Connection) -> str:
    """
    insert new user into database

    Args:
        usr (user_req): model containing user email and password
        conn (Connection): database connection

    Raises:
        HTTPException: ConflictError if user already exists
        HTTPException: InternalError if database query fails

    Returns:
        str: JWT token
    """
    # create new user model from request data
    new_usr: user = usr.new_user()
    try:
        # insert new user into database and return JWT token
        await repo.insert_user(new_usr, conn)
        return jwt.encode(
            payload={"user_id": str(new_usr.user_id), "role": new_usr.role},
            key=os.environ.get("JWT_SECRET"),
        )
    except ConflictError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=e.msg)
    except InternalError as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=e.msg)
    