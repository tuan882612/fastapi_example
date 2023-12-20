
from asyncpg import Connection, InternalServerError, UniqueViolationError, Record
from pydantic import EmailStr
import structlog
from src.exceptions import ConflictError, InternalError, NotFoundError
from src.auth.models import user, user_cred

async def get_user_cred(email: EmailStr, conn: Connection) -> user_cred:
    """
    Retrieve user credentials from database

    Args:
        email (EmailStr): user email
        conn (Connection): database connection

    Raises:
        NotFoundError: self explanatory
        InternalError: self explanatory

    Returns:
        user_cred: user credentials containing user_id, password, and role
    """
    query: str = "SELECT user_id, password, role FROM public.users WHERE email = $1"
    try:
        record: Record = await conn.fetchrow(query, email)
        if not record:
            raise NotFoundError("User not found")
        
        return user_cred(**record)
    except InternalServerError:
        structlog.get_logger().error(f"Failed to retrieve user credentials")
        raise InternalError("Failed to retrieve user credentials")
    

async def insert_user(usr: user, conn: Connection) -> None:
    """
    Insert new user into database

    Args:
        usr (user): user model containing user_id, email, password, role, and created
        conn (Connection): database connection

    Raises:
        ConflictError: self explanatory
        InternalError: self explanatory
    """
    query: str = "INSERT INTO public.users (user_id, email, password, created, role) VALUES ($1, $2, $3, $4, $5)"
    try:
        await conn.execute(query, usr.user_id, usr.email, usr.password, usr.created, usr.role)
    except UniqueViolationError as e:
        raise ConflictError("User already exists")
    except InternalServerError:
        structlog.get_logger().error(f"Failed to insert user: {e}")
        raise InternalError("Failed to insert user")