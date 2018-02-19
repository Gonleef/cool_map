import json
import logging
from http import HTTPStatus

from clients.auth_provider import IAuthProvider
from core.entities import FailResult, Permission, ItemsResult
from core.http_headers import HTTPHeaders
from core.operation_result import OperationResult
from pyramid.request import Request


class PermissionClient(object):
    def __init__(self, auth: IAuthProvider):
        self.auth = auth

    def get_permissions(self, skip: int = 0, take: int = 50000):
        request = Request.blank('/api/permissions/v1/list?skip=%s&take=%s' % (skip, take))
        request.authorization = self.auth.get_session_id()
        return self._get_permissions(request)

    def get_permission(self, obj: str):
        request = Request.blank('/api/permissions/v1/object/%s' % obj)
        request.authorization = self.auth.get_session_id()
        return self._get_permission(request, ' to object ' + obj)

    def get_user_permission(self, user_id: str, obj: str):
        request = Request.blank('/api/permissions/v1/user/%s/object/%s' % (user_id, obj))
        request.authorization = self.auth.get_session_id()
        return self._get_permission(request, ' for user %s to object %s' % (user_id, obj))

    @staticmethod
    def _get_permission(request: Request, help: str = ''):
        response = request.get_response()
        data = json.loads(response.body.decode())
        if response.status_code not in [HTTPStatus.OK.value, HTTPStatus.NOT_FOUND.value]:
            logging.warning('Fail to get permissions' + help + ': ' + data.get('error_message', ''))
            return OperationResult.fail(FailResult(code=response.status_code, **data))
        return OperationResult.success(Permission(**data))

    @staticmethod
    def _get_permissions(request: Request, help: str = ''):
        response = request.get_response()
        data = json.loads(response.body.decode())
        if response.status_code != HTTPStatus.OK and response.status_code != HTTPStatus.NOT_FOUND:
            logging.warning('Fail to load permissions' + help + ': ' + data.get('error_message', ''))
            return OperationResult.fail(FailResult(code=response.status_code, **data))
        data['items'] = list(map(lambda o: Permission(**o), data.get('items', [])))
        return OperationResult.success(ItemsResult(**data))
