from admin.configuration import Configuration
from clients.auth_provider import SessionAuthProvider
from core.auth_policy import CookieAuthenticationPolicy, AuthorizationPolicy
from core.permissions import Permissions
from core.response import HTTPTemporaryRedirect
from pyramid.config import Configurator


def get_app(global_config, **settings):
    Configuration.init(**settings)
    auth = SessionAuthProvider(Configuration.Sid)

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('core_static', 'core:static', cache_max_age=3600)
    config.add_route('index', '/', factory=lambda r: 'global:index')
    config.add_route('create', '/create', factory=lambda r: 'global:create')
    config.scan()
    config.set_default_permission(Permissions.Auth)
    config.set_authentication_policy(CookieAuthenticationPolicy())
    config.set_authorization_policy(AuthorizationPolicy(auth))
    """config.add_forbidden_view(lambda r: HTTPTemporaryRedirect('/'))"""
    config.add_notfound_view(lambda r: HTTPTemporaryRedirect('/'))
    return config.make_wsgi_app()
