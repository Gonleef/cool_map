from api.auth_api import AuthApi
from api.base_api_configuration import not_found_view, forbidden_view, exception_view
from api.configuration import Configuration
from api.form_api import FormApi
from api.permissions_api import PermissionApi
from clients.auth_provider import SessionAuthProvider
from core.auth_policy import HeaderAuthenticationPolicy, AuthorizationPolicy
from core.permissions import Permissions
from pyramid.config import Configurator


def get_app(global_config, **settings):
    Configuration.init(**settings)
    auth = SessionAuthProvider(Configuration.Sid)

    config = Configurator(settings=settings)
    config.include(AuthApi, route_prefix='/auth')
    config.include(FormApi, route_prefix='/form')
    config.include(PermissionApi, route_prefix='/permissions')

    config.add_notfound_view(not_found_view)
    config.add_forbidden_view(forbidden_view)
    config.add_exception_view(exception_view)
    config.set_default_permission(Permissions.Api)
    config.set_authentication_policy(HeaderAuthenticationPolicy())
    config.set_authorization_policy(AuthorizationPolicy(auth))
    return config.make_wsgi_app()
