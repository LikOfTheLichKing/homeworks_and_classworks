from werkzeug.exceptions import HTTPException


class UserResponsError(HTTPException):
    code = 400


class EnoughtUserPermission(HTTPException):
    code = 403
