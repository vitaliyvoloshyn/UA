from pydantic import BaseModel, EmailStr, Field


class UserAddDTO(BaseModel):
    first_name: str = Field(min_length=1, max_length=20)
    last_name: str = Field(min_length=1, max_length=20)
    email: EmailStr
    password: str = Field(min_length=1, max_length=20)


class UserDTO(UserAddDTO):
    id: int
