from pydantic import BaseModel, EmailStr, Field


class UserSignInDTO(BaseModel):
    email: EmailStr
    password: str | bytes = Field(min_length=1, max_length=50)


class UserAddDTO(UserSignInDTO):
    first_name: str = Field(min_length=1, max_length=20)
    last_name: str = Field(min_length=1, max_length=20)


class UserDTO(UserAddDTO):
    id: int
