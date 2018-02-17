import json
import socket
from http import HTTPStatus

from core.entities import SessionState, FailResult
from core.http_method import HTTPMethod
from core.operation_result import OperationResult
from pyramid.request import Request


class AuthClient(object):
    _my_ip: str = None

    def get_session(self, auth_sid: str):
        request = Request.blank('/api/auth/v1/session/' + auth_sid)
        response = request.get_response()
        data = json.loads(response.body.decode())
        return OperationResult.success(SessionState(**data)) if response.status_code == HTTPStatus.OK \
            else OperationResult.fail(FailResult(code=response.status_code))

    def authenticate_by_pass(self, login: str, password: str, client_addr: str = None):
        client_addr = client_addr if client_addr else AuthClient._get_ip()
        request = Request.blank('/api/auth/v1/authenticate_by_pass?login=%s&client_addr=%s' % (login, client_addr))
        request.body = password.encode()
        request.method = HTTPMethod.POST.value
        response = request.get_response()
        data = json.loads(response.body.decode())
        return OperationResult.success(data.get('sid')) if response.status_code == HTTPStatus.OK \
            else OperationResult.fail(FailResult(code=response.status_code, **data))

    @classmethod
    def _get_ip(cls):
        if not cls._my_ip:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('google.com', 0))
            cls._my_ip = s.getsockname()[0]
        return cls._my_ip
