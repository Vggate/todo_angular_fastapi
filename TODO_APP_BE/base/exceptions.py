from values import HttpStatusCode


class Error(Exception):
    http_code = HttpStatusCode.InternalServerError
    name = None

    def __init__(self, msg: str = None, code: str = None):
        self.msg = msg
        self.code = code

    def to_json(self):
        return {
            'error': {
                'code': self.code,
                'name': self.name,
                'message': self.msg
            }
        }

    def __repr__(self):
        return f'{self.code or "N/A"} - {self.name or "N/A"}: {self.msg or "N/A"}'


class ValidationError(Error):
    name = 'ValidationError'
    http_code = HttpStatusCode.UnprocessableContent


class UserError(ValidationError):
    name = 'UserError'


class RecordNotFoundError(Error):
    name = 'RecordNotFound'
    http_code = HttpStatusCode.NotFound


class AuthenticationError(Error):
    name = 'AuthenticationError'
    http_code = HttpStatusCode.UnAuthorized


class AccessError(Error):
    name = 'PermissionDenied'
    http_code = HttpStatusCode.Forbidden
