import asyncio
import logging
import traceback
from functools import wraps
from typing import Optional

from starlette.requests import Request as BaseRequest
from starlette.responses import JSONResponse

from base.database import ConnectionPool
from base.exceptions import Error
from base.models import Environment
from values import HttpStatusCode

logger = logging.getLogger(__name__)


class Request(BaseRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env: Optional[Environment] = None


def session_handler(func):
    @wraps(func)
    def sync_wrapper(*args, **kwargs) -> JSONResponse:
        request: Request = kwargs['request']
        db_session = ConnectionPool.new_session()
        request.env = Environment(db_session=db_session)
        try:
            resp = func(*args, **kwargs)
            db_session.commit()
        except Error as e:
            db_session.rollback()
            traceback.print_exc()
            logger.error(e.__repr__(), exc_info=True)
            resp = JSONResponse(content=e.to_json(), status_code=e.http_code)
        except Exception as e:
            db_session.rollback()
            traceback.print_exc()
            logger.error(e.__repr__(), exc_info=True)
            resp = JSONResponse(content={'error': {'name': 'UnknownError', 'msg': None, 'code': None}},
                                status_code=HttpStatusCode.InternalServerError)
        finally:
            db_session.close()
        return resp

    @wraps(func)
    async def async_wrapper(*args, **kwargs) -> JSONResponse:
        request: Request = kwargs['request']
        db_session = ConnectionPool.new_session(user=None, is_sudo=True)
        request.env = Environment(db_session=db_session)
        try:
            resp = func(*args, **kwargs)
            db_session.commit()
        except Error as e:
            db_session.rollback()
            traceback.print_exc()
            logger.error(e.__repr__(), exc_info=True)
            resp = JSONResponse(content=e.to_json(), status_code=e.http_code)
        except Exception as e:
            db_session.rollback()
            traceback.print_exc()
            logger.error(e.__repr__(), exc_info=True)
            resp = JSONResponse(content={'error': {'name': 'UnknownError', 'msg': None, 'code': None}},
                                status_code=HttpStatusCode.InternalServerError)
        finally:
            db_session.close()
        return resp

    if asyncio.iscoroutine(func):
        return async_wrapper
    else:
        return sync_wrapper