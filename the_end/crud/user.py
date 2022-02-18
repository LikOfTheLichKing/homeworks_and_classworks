from unicodedata import name
from models.user import RegistrationModel, UserModel
import sqlite3
import uuid
from core.password_hash import passwords_equal, hash_password
from werkzeug.datastructures import Authorization
from core.errors.auth_errors import AuthError
from core.errors.registration_errors import UserExistsError
from typing import Any


def get(conn: sqlite3.Connection, login: str) -> UserModel | None:
    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name FROM User WHERE name=?", (login,))
        row = cur.fetchone()

        if row is None:
            return None

        return UserModel(id=row[0], login=row[1])
    finally:
        cur.close()


class UserCRUD:
    def create(
            conn: sqlite3.Connection, data: RegistrationModel
            ) -> None:
        cur = conn.cursor()
        try:
            user = get(conn, data.login)
            if user is not None:
                raise UserExistsError(
                    f"User with login {data.login} already exists"
                    )

            user_id = uuid.uuid4()
            cur.execute(
                "INSERT INTO USER VALUES(?, ?, ?)",
                (
                    str(user_id),
                    data.login,
                    hash_password(data.password)
                ),
            )
        finally:
            cur.close()

    def authenticate(
                conn: sqlite3.Connection, auth_data: Authorization
            ) -> None:
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT password FROM USER WHERE name=?", (
                    auth_data.username,
                    )
            )
            row = cur.fetchone()

            if row is None:
                raise AuthError("User does not exist")

            password_hashed = row[0]

            if not passwords_equal(
                                    auth_data.password, password_hashed
                                ):
                raise AuthError("Password is incorrect")
        finally:
            cur.close()

    def get(conn: sqlite3.Connection, login: str) -> UserModel | None:
        cur = conn.cursor()

        try:
            cur.execute(
            "SELECT id, name FROM User WHERE name=?",
            (str(login),)
            )
            row = cur.fetchone()

            if row is None:
                return None

            return UserModel(id=row[0], login=row[1])
        finally:
            cur.close()

    def delete(conn: sqlite3.Connection, auth_data: Authorization):
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT password FROM USER WHERE name=?", (
                    auth_data.username,
                    )
            )
            row = cur.fetchone()

            if row is None:
                raise AuthError("User does not exist")

            password_hashed = row[0]

            if not passwords_equal(
                                    auth_data.password, password_hashed
                                ):
                raise AuthError("Password is incorrect")
            cur.execute(
                "SELECT id FROM USER WHERE name=?",
                (auth_data.username,)
            )
            id = cur.fetchone()[0]
            cur.execute("DELETE FROM User WHERE id=?", (id,))
            cur.execute(
                "SELECT id FROM POLLS WHERE creatorId=?",
                (id,)
                )
            users_polls = cur.fetchall()
            cur.execute(
                "DELETE FROM POLLS WHERE creatorId=?",
                (id,)
            )
            answers_id = []
            if users_polls is not None:
                for survey_id in users_polls:
                    cur.execute(
                            "SELECT id FROM ANSWERS WHERE surveyId=?",
                            (survey_id,)
                        )
                    answers = cur.fetchone()
                    for i in range(len(answers)):
                        answers_id.append(answers[(i-1)])
                    cur.execute(
                        "DELETE FROM ANSWERS WHERE surveyId=?",
                        (survey_id,)
                        )
                for answer_id in answers_id:
                    cur.execute(
                        "DELETE FROM USER_RESPONSES WHERE answerId=?",
                        (answer_id,)
                        )
                cur.execute(
                    "DELETE FROM USER_RESPONSES WHERE userId=?",
                    (id,)
                )
            cur.execute(
                "DELETE FROM FOLLOWS WHERE (follower_id=?) OR (followed_id=?",
                (id, id,)
            )
        finally:
            cur.close()

    def follow(
        conn: sqlite3.Connection, follower_id: str, followed_id: str
    ):
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT name FROM USER WHERE id=?",
                (followed_id,)
            )
            UserCRUD.get(conn, name)
            cur.execute(
                "SELECT followed_id FROM FOLLOWS WHERE (follower_id=?) AND (followed_id=?)",
                (follower_id, followed_id,)
            )
            users_relations = cur.fetchall()
            if users_relations is None:
                cur.execute(
                    "INSERT INTO FOLLOWS VALUES(?, ?)",
                    (follower_id, followed_id,)
                )
            else:
                cur.execute(
                    "DELETE FROM FOLLOWS WHERE (follower_id=?) AND (followed_id=?)",
                    (follower_id, followed_id,)
                )
        finally:
            cur.close()

    def get_follows_list(
        conn: sqlite3.Connection, user_id: str
    ) -> Any:
        cur = conn.cursor()
        response = None
        try:
            cur.execute(
                "SELECT followed_id FROM FOLLOWS WHERE (follower_id=?) OR (followed_id=?)",
                (user_id, user_id,)
            )
            response = cur.fetchone()
        finally:
            cur.close()
        return response
