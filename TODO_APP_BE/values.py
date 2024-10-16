from enum import Enum


class HttpStatusCode(int, Enum):
    OK = 200
    BadRequest = 400
    UnAuthorized = 401
    Forbidden = 403
    NotFound = 404
    MethodNotAllow = 405
    UnprocessableContent = 422
    InternalServerError = 500