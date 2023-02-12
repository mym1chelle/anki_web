import typing

from pydantic import BaseModel
from typing import Optional


class Login(BaseModel):
    auth_token: Optional[str]
    non_field_errors: Optional[typing.List[str]]


class Registration(BaseModel):
    email: Optional[str]
    username: Optional[str] | Optional[typing.List[str]]
    password: Optional[str] | Optional[typing.List[str]]
    id: Optional[int]


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