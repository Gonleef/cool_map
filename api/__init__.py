from api.auth_api import AuthApi
from api.base_api_configuration import not_found_view, forbidden_view, exception_view
from api.form_api import FormApi
from api.permissions_api import PermissionApi
from api.users_api import UsersApi
from core.auth_policy import HeaderAuthenticationPolicy, AuthorizationPolicy
from core.configuration import ConfigurationWrapper
from core.permissions import Permissions
from pyramid.config import Configurator


def get_app(global_config, **settings):
    ConfigurationWrapper.init(**settings)

    config = Configurator(settings=settings)
    config.include(AuthApi, route_prefix='/auth')
    config.include(UsersApi, route_prefix='/users')
    config.include(PermissionApi, route_prefix='/permissions')
    config.include(FormApi, route_prefix='/form')

    config.add_notfound_view(not_found_view)
    config.add_forbidden_view(forbidden_view)
    config.add_exception_view(exception_view)
    config.set_default_permission(Permissions.Auth)
    config.set_authentication_policy(HeaderAuthenticationPolicy())
    config.set_authorization_policy(AuthorizationPolicy(ConfigurationWrapper.get_auth()))
    return config.make_wsgi_app()
