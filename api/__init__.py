from api.base_api_configuration import not_found_view, forbidden_view, exception_view
from core.auth_policy import HeaderAuthenticationPolicy, AuthorizationPolicy
from core.configuration import ConfigurationWrapper
from core.permissions import Permissions
from pyramid.config import Configurator


def get_app(global_config, **settings):
    ConfigurationWrapper.init('api', **settings)

    config = Configurator(settings=settings)
    config.include('api.auth_api', route_prefix='/auth')
    config.include('api.users_api', route_prefix='/users')
    config.include('api.permissions_api', route_prefix='/permissions')
    config.include('api.form_api', route_prefix='/form')
    config.include('api.places_api', route_prefix='/places')
    config.add_notfound_view(not_found_view)
    config.add_forbidden_view(forbidden_view)
    config.add_exception_view(exception_view)
    config.set_default_permission(Permissions.Auth)
    config.set_authentication_policy(HeaderAuthenticationPolicy())
    config.set_authorization_policy(AuthorizationPolicy(ConfigurationWrapper.get_auth('api')))
    return config.make_wsgi_app()
