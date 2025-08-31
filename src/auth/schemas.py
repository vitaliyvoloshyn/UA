from pydantic import BaseModel, EmailStr


class UserAddDTO(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserDTO(UserAddDTO):
    id: int
