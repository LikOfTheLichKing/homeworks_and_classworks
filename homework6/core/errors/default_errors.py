from werkzeug.exceptions import HTTPException


class ForbiddenError(HTTPException):
    code = 403


class NotFoundError(HTTPException):
    code = 404


class InvalidDataFormat(HTTPException):
    code = 422


class ConflictError(HTTPException):
    code = 409
