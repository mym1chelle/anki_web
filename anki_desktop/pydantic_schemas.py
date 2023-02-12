from pydantic import BaseModel
import typing


class Login(BaseModel):
    auth_token: typing.Optional[str]
    non_field_errors: typing.Optional[typing.List[str]]


class Registration(BaseModel):
    email: typing.Optional[str]
    username: typing.Optional[str] | typing.Optional[typing.List[str]]
    password: typing.Optional[str] | typing.Optional[typing.List[str]]
    id: typing.Optional[int]


class Deck(BaseModel):
    id: int
    name: str


class Style(BaseModel):
    id: int
    name: str


class Decks(BaseModel):
    decks: typing.List[Deck]


class Styles(BaseModel):
    styles: typing.List[Style]