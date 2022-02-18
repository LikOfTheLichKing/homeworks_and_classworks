from asyncio.windows_events import NULL
import sqlite3
from typing import Any
import uuid
from crud.user import UserCRUD
from models.survey import CreationSurveyModel
from werkzeug.datastructures import Authorization
from core.errors.user_responses_error import UserResponsError
from core.errors.user_responses_error import EnoughtUserPermission
from core.errors.polls_errors import IncorrectSurveyIdError


class SurveyCrud:
    def create(
        conn: sqlite3.Connection,
        data: CreationSurveyModel,
        auth_data: Authorization
    ) -> None:
        cur = conn.cursor()
        try:
            if data.privacy:
                privacy = 1
            else:
                privacy = 0
            UserCRUD.authenticate(conn, auth_data)
            cur.execute(
                "SELECT id FROM USER WHERE name=?", (auth_data.username,)
            )
            creator_id = cur.fetchone()[0]
            survey_id = str(uuid.uuid4())
            cur.execute(
                "INSERT INTO POLLS VALUES(?, ?, ?, ?, ?)",
                (
                    creator_id,
                    survey_id,
                    data.name,
                    data.description,
                    privacy,
                )
            )
            for answer in data.answers:
                answer_id = str(uuid.uuid4())
                cur.execute(
                    "INSERT INTO ANSWERS VALUES(?, ?, ?)",
                    (answer, answer_id, survey_id)
                )
        finally:
            cur.close()

    def add_user_answer(
        conn: sqlite3.Connection, answer_id, auth_data: Authorization
    ) -> None:
        cur = conn.cursor()
        try:
            UserCRUD.authenticate(conn, auth_data)
            cur.execute(
                "SELECT id FROM USER WHERE name=?", (auth_data.username,)
            )
            user_id = cur.fetchone()[0]
            cur.execute(
                "SELECT surveyId FROM ANSWERS WHERE id=?", (str(answer_id),)
            )
            checking_data = cur.fetchone()
            if checking_data is not None:
                survey_id = checking_data[0]
            else:
                raise UserResponsError("incorrect answer id")
            cur.execute(
                "DELETE FROM USER_RESPONSES WHERE (userId=?) AND (surveyId=?)",
                (user_id, survey_id,)
            )
            cur.execute(
                "INSERT INTO USER_RESPONSES VALUES(?, ?, ?)",
                (user_id, answer_id, survey_id)
            )
        finally:
            cur.close()

    def delete_survey(
        conn: sqlite3.Connection, survey_id, auth_data: Authorization
    ) -> None:
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT id FROM USER WHERE name=?",
                (auth_data.username,)
                )
            id = cur.fetchone()[0]
            cur.execute(
                "SELECT creatorId FROM POLLS WHERE id=?",
                (survey_id,)
                )

            creator_id = cur.fetchone()
            if creator_id is None:
                raise IncorrectSurveyIdError("incorrect survay id")
            creator_id = creator_id[0]
            if creator_id != id:
                raise EnoughtUserPermission("It`s not your post")
            cur.execute(
                "DELETE FROM POLLS WHERE id=?",
                (survey_id,)
                )
            cur.execute(
                "DELETE FROM ANSWERS WHERE surveyId=?",
                (survey_id,)
                )
            cur.execute(
                "DELETE FROM USER_RESPONSES WHERE surveyId=?",
                (survey_id,)
                )
        finally:
            cur.close()

    def get_survey(
        conn: sqlite3.Connection, survey_id
    ) -> dict:
        cur = conn.cursor()
        total_response = {}
        try:
            cur.execute(
                "SELECT name, description, creatorId FROM POLLS WHERE id=?",
                (survey_id,)
            )
            row = cur.fetchone()
            if row is None:
                raise IncorrectSurveyIdError("Incorrect survey id")
            name = row[0]
            description = row[1]

            cur.execute(
                "SELECT creatorId FROM POLLS WHERE id=?",
                (survey_id,)
            )
            creator_id = cur.fetchone()[0]
            cur.execute("SELECT name FROM USER WHERE id=?", (creator_id,))
            author = cur.fetchone()[0]
            cur.execute(
                "SELECT name FROM ANSWERS WHERE surveyId=?",
                (survey_id,)
            )
            answers_names = cur.fetchone()

            cur.execute(
                "SELECT id FROM ANSWERS WHERE surveyId=?",
                (survey_id,)
            )
            answers_id = cur.fetchone()
            answers_response = {}
            for i in range(len(answers_id)):
                i = i-1
                cur.execute(
                    "SELECT COUNT(*) FROM USER_RESPONSES WHERE answerId=?",
                    (answers_id[i],)
                )
                count = cur.fetchone()
                if count is NULL:
                    count = 0
                answers_response[answers_id[i]] = {
                    "name": answers_names[i],
                    "voites": count
                }
            cur.execute(
                    "SELECT COUNT(*) FROM USER_RESPONSES WHERE surveyId=?",
                    (survey_id,)
                )
            total_counts = cur.fetchone()[0]
            total_response["id"] = survey_id
            total_response["name"] = name
            total_response["description"] = description
            total_response["creator"] = author
            total_response["total voites"] = total_counts
            total_response["answers"] = answers_response
        finally:
            cur.close()
        return(
            total_response
        )

    def get_polls_list(
        conn: sqlite3.Connection
    ) -> Any:
        cur = conn.cursor()
        response = None
        try:
            cur.execute(
                "SELECT id, name FROM POLLS WHERE privacy=?",
                (0,)
            )
            response = cur.fetchone()
        finally:
            cur.close()
        return response

    def get_polls_by_followed(
        self, conn: sqlite3.Connection, auth_data: Authorization
    ) -> list[dict] | None:
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT id FROM USER WHERE name=?",
                (auth_data.username,)
                )
            id = cur.fetchone()[0]
            cur.execute(
                "SELECT followed_id FROM FOLLOWS WHERE follower_id=?",
                (id)
                )
            response = []
            followed_list = cur.fetchone()
            for i in followed_list:
                cur.execute(
                    "SELECT id, name FROM POLLS WHERE (creatorId=?) AND (privacy=0)",
                    (i,)
                )
                polls = cur.fetchone()
                response.append(polls)
            return(response)
        finally:
            cur.close()

    def get_polls_by_user(
        self,
        conn: sqlite3.Connection,
        user_id
    ) -> list[dict] | None:
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT id, name FROM POLLS WHERE (creatorId=?) AND (privacy=0)",
                (user_id,)
                )
            polls = cur.fetchone()
            return polls
        finally:
            cur.close()
