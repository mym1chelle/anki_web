from pydantic import BaseModel
from pydantic import types as t
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


class Decks(BaseModel):
    count: int
    next: typing.Optional[str]
    previous: typing.Optional[str]
    results: typing.List[Deck]


class Style(BaseModel):
    id: int
    name: str


class Styles(BaseModel):
    styles: typing.List[Style]


class CardTodayResult(BaseModel):
    id: int
    question: typing.Text
    question_type: str
    answer: typing.Text
    answer_type: str
    style: str


class GetCardToday(BaseModel):
    count: int
    next: typing.Optional[str]
    previous: typing.Optional[str]
    results: typing.List[CardTodayResult]


class GetCardAnswer(BaseModel):
    id: int
    easiness: typing.Optional[float]
    interval: typing.Optional[int]
    repetitions: typing.Optional[int]
    review_date: t.OptionalDate


class CreateDeckResult(BaseModel):
    name: str | typing.List[str]


class CreateCardResult(BaseModel):
    question: typing.Optional[str] | typing.Optional[typing.List[str]]
    question_type: typing.Optional[str]
    answer: typing.Optional[str] | typing.Optional[typing.List[str]]
    answer_type: typing.Optional[str]
    style: typing.Optional[int]
    deck: typing.Optional[int]
