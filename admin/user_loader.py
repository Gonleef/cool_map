import logging

from clients.api_client import ApiClient
from core.auth_policy import AuthorizationPolicy
from core.configuration import ConfigurationWrapper
from core.entities import User
from pyramid.request import Request


def load_user(request: Request) -> User:
    client = ApiClient(ConfigurationWrapper.get_auth('admin'))
    if not (hasattr(request, 'session') and request.session is not None):
        AuthorizationPolicy(ConfigurationWrapper.get_auth('admin')).authenticated_userid(request)
    if hasattr(request, 'session') and request.session is not None:
        result = client.users_client.load(request.session.user_id)
        if not result.is_success:
            logging.warning("Fail to load user for session '" + request.session.session_id + "': " + result.data.message)
            raise Exception(result.data)
        return result.data
    return None
