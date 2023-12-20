import bcrypt
import datetime
import enum
from pydantic import BaseModel, EmailStr
import uuid

class roles(str, enum.Enum):
    base: str = "base"
    admin: str = "admin"

class user(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    password: bytes
    role: roles
    created: datetime.datetime

class user_cred(BaseModel):
    user_id: uuid.UUID
    password: bytes
    role: roles
    
class user_req(BaseModel):
    email: EmailStr
    password: str
    
    def new_user(self) -> user:
        return user(
            user_id=uuid.uuid4(),
            email=self.email,
            password=bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt()),
            role="base",
            created=datetime.datetime.utcnow()
        )
