import json
from http import HTTPStatus

from core.entities import SessionState, FailResult
from core.http_method import HTTPMethod
from core.operation_result import OperationResult
from pyramid.request import Request


class AuthClient(object):
    def get_session(self, auth_sid: str):
        request = Request.blank('/api/auth/v1/session/' + auth_sid)
        response = request.get_response()
        data = json.loads(response.body.decode())
        return OperationResult.success(SessionState(**data)) if response.status_code == HTTPStatus.OK \
            else OperationResult.fail(FailResult(http_code=response.status_code, **data))

    def authenticate_by_pass(self, login: str, password: str):
        request = Request.blank('/api/auth/v1/authenticate_by_pass?login=' + login)
        request.body = password.encode()
        request.method = HTTPMethod.POST.value
        response = request.get_response()
        data = json.loads(response.body.decode())
        return OperationResult.success(data.get('sid')) if response.status_code == HTTPStatus.OK \
            else OperationResult.fail(FailResult(http_code=response.status_code, **data))
