import json
from http import HTTPStatus

from clients.auth_provider import IAuthProvider
from core.entities import FailResult, User
from core.http_headers import HTTPHeaders
from core.operation_result import OperationResult
from pyramid.request import Request


class UsersClient(object):
    def __init__(self, auth: IAuthProvider):
        self.auth = auth

    def load(self, user_id: str):
        request = Request.blank('api/users/v1/user/' + user_id)
        request.headers = {HTTPHeaders.AUTHORIZATION.value: self.auth.get_session_id()}
        response = request.get_response()
        data = json.loads(response.body.decode())
        return OperationResult.success(User(**data)) if response.status_code == HTTPStatus.OK \
            else OperationResult.fail(FailResult(code=response.status_code, **data))
