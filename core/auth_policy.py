import logging

from clients.api_client import ApiClient
from clients.auth_provider import IAuthProvider
from core.http_headers import HTTPHeaders
from core.permissions import Permissions
from pyramid.request import Request


class HeaderAuthenticationPolicy(object):
    def effective_principals(self, request: Request):
        auth_sid = request.headers.get(HTTPHeaders.AUTHORIZATION.value)
        setattr(request, 'auth_sid', auth_sid)
        return request


class CookieAuthenticationPolicy(object):
    def effective_principals(self, request: Request):
        auth_sid = request.cookies.get('auth.sid')
        setattr(request, 'auth_sid', auth_sid)
        return request


class AuthorizationPolicy(object):
    def __init__(self, auth: IAuthProvider):
        self.api_client = ApiClient(auth)

    def permits(self, context, request: Request, permission: Permissions):
        if permission is None or permission == permission.Null:
            return True
        if request.auth_sid is None:
            return False

        self.authenticated_userid(request)
        if request.session is None:
            return False
        if permission == Permissions.Auth:
            return True
        return permission in self.get_permissions(context, request)

    def authenticated_userid(self, request: Request) -> None:
        result = self.api_client.auth_client.get_session(request.auth_sid)
        if not result.is_success:
            logging.warning("Fail to get auth.sid: " + result.data.error_message)
            setattr(request, 'session', None)
        else:
            setattr(request, 'session', result.data)

    def get_permissions(self, context, request: Request) -> Permissions:
        all_result = self.api_client.permission_client.get_user_permission(request.session.user_id, 'global:all')
        if not all_result.is_success:
            return Permissions.Null
        context_result = self.api_client.permission_client.get_user_permission(request.session.user_id, context)
        if not context_result.is_success:
            return Permissions.Null
        return all_result.data.value | context_result.data.value
