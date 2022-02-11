from werkzeug.exceptions import HTTPException


class IncorrectSurveyIdError(HTTPException):
    code = 400
