import logging

from clients.api_client import ApiClient
from clients.auth_provider import IAuthProvider
from core.configuration import Configuration
from core.http_headers import HTTPHeaders
from core.permissions import Permissions
from core.urn import Urn
from pyramid.request import Request


class HeaderAuthenticationPolicy(object):
    def effective_principals(self, request: Request):
        auth_sid = request.headers.get(HTTPHeaders.AUTHORIZATION.value)
        setattr(request, 'auth_sid', auth_sid)
        setattr(request, 'session', None)
        setattr(request, 'user', None)
        return request


class CookieAuthenticationPolicy(object):
    def effective_principals(self, request: Request):
        auth_sid = request.cookies.get('auth.sid')
        setattr(request, 'auth_sid', auth_sid)
        setattr(request, 'session', None)
        return request


class AuthorizationPolicy(object):
    def __init__(self):
        self.client = ApiClient(Configuration.get_auth())

    def permits(self, obj: Urn, request: Request, permission: Permissions):
        if permission is None or permission == permission.Null:
            return True

        self.authenticated_userid(request)
        if request.session is None:
            return False
        if permission == Permissions.Auth:
            return True

        permissions_result = self.client.permission_client\
            .get_user_permission(request.session.user_id, obj)
        if not permissions_result.is_success:
            return Permissions.Null
        return permission in permissions_result.data

    def authenticated_userid(self, request: Request):
        if not hasattr(request, 'auth_sid') or request.auth_sid is None:
            return

        result = self.client.auth_client.get_session(request.auth_sid)
        if not result.is_success:
            logging.warning("Fail to load session: " + request.auth_sid)
            return
        setattr(request, 'session', result.data)
