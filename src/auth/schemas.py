from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserSignInDTO(BaseModel):
    email: EmailStr
    password: str | bytes = Field(min_length=1)


class UserAddDTO(UserSignInDTO):
    first_name: str = Field(min_length=1, max_length=20)
    last_name: str = Field(min_length=1, max_length=20)
    avatar: Optional[str] = None


class UserDTO(UserAddDTO):
    id: int
    is_active: bool = True
    is_admin: bool = False


class TokenInfo(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
