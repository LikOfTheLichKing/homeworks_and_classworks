from asyncio.windows_events import NULL
import sqlite3
import uuid
from flask import request
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
            UserCRUD.authenticate(conn, auth_data)
            cur.execute(
                "SELECT id FROM USER WHERE name=?", (auth_data.username,)
            )
            creator_id = cur.fetchone()[0]
            survey_id = str(uuid.uuid4())
            cur.execute(
                "INSERT INTO POLLS VALUES(?, ?, ?, ?)",
                (creator_id, survey_id, data.name, data.description)
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
                "SELECT userId FROM USER_RESPONSES WHERE surveyId=?",
                (survey_id,)
            )
            checking_data = cur.fetchone()
            if checking_data is not None:
                for user in checking_data:
                    if user == user_id:
                        raise UserResponsError(
                            "You can`t change your answer after voiting"
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
            auth_data = request.authorization

            cur.fetchone(
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
            answers_id = []
            cur.execute(
                "SELECT id FROM ANSWERS WHERE surveyId=?",
                (survey_id)
                )
            answers = cur.fetchone()
            for i in range(len(answers)):
                answers_id.append(answers[(i-1)])
            cur.execute(
                "DELETE FROM POLLS WHERE id=?",
                (survey_id,)
                )
            cur.execute(
                "DELETE FROM ANSWERS WHERE surveyId=?",
                (survey_id,)
                )
            for answer_id in answers_id:

                
    