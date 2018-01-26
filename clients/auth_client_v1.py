import json
from http import HTTPStatus

from clients.auth_provider import IAuthProvider
from core.entities import SessionState, FailResult
from core.operation_result import OperationResult
from pyramid.request import Request


class AuthClient(object):
    def __init__(self, auth: IAuthProvider):
        self.auth = auth

    def get_session(self, auth_sid: str):
        request = Request.blank('/api/auth/v1/session/' + auth_sid)
        response = request.get_response()
        data = json.loads(response.body.decode())
        return OperationResult.success(SessionState(**data)) if response.status_code == HTTPStatus.OK \
            else OperationResult.fail(FailResult(http_code=response.status_code, **data))
