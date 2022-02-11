from flask import request
import sqlite3
from typing import Iterator
from contextlib import contextmanager
from core import errors
from schemas.user import UserModel
from pydantic import BaseModel
from crud import UserCRUD as user_crud

DB_FILE = "data/db"


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(DB_FILE)
    yield conn
    conn.commit()


def get_current_user() -> UserModel:
    auth_data = request.authorization
    if auth_data is None:
        raise errors.AuthError("Auth headers not provided")

    with get_connection() as conn:
        user_data = user_crud.authenticate(conn, auth_data)

    return user_data


def get_user_by_login(login: str) -> UserModel:
    with get_connection() as conn:
        user_data = user_crud.get(conn, login)

    if user_data is None:
        raise errors.NotFoundError(f"User with login '{login}' does not exist")

    return user_data


def get_input(ModelType) -> BaseModel:
    data = request.get_json(True)
    if data is None:
        raise errors.InvalidDataFormat("data in .json format not found")

    return ModelType(**data)
