from core.auth_policy import CookieAuthenticationPolicy, AuthorizationPolicy
from core.configuration import ConfigurationWrapper
from core.permissions import Permissions
from core.response import HTTPTemporaryRedirect
from pyramid.config import Configurator


def get_app(global_config, **settings):
    ConfigurationWrapper.init(**settings)

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('admin_sstatic', 'admin:static', cache_max_age=3600)
    config.add_static_view('core_static', 'core:static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('answers', '/answer')
    config.add_route('answer', '/answer/{answer_id}')
    config.add_route('forms', '/form')
    config.add_route('form', '/form/{form_id}')
    config.add_route('user', '/user')
    config.add_route('user_permissions', '/permissions')
    config.scan()
    config.set_default_permission(Permissions.Auth)
    config.set_authentication_policy(CookieAuthenticationPolicy())
    config.set_authorization_policy(AuthorizationPolicy(ConfigurationWrapper.get_auth()))
    """config.add_forbidden_view(lambda r: HTTPTemporaryRedirect('/admin'))"""
    config.add_notfound_view(lambda r: HTTPTemporaryRedirect('/admin'))
    return config.make_wsgi_app()
