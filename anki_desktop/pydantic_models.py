from pydantic import BaseModel


class Login(BaseModel):
    auth_token: str


# class Message(BaseModel):
#     from_user: User
