from clients.auth_provider import LoginAuthProvider
from core.auth_policy import CookieAuthenticationPolicy, AuthorizationPolicy
from core.configuration import Configuration
from core.permissions import Permissions
from core.response import HTTPTemporaryRedirect
from core.urns import Urns
from pyramid.config import Configurator


def get_app(global_config, **settings):
    Configuration.init(**settings)

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('core_static', 'core:static', cache_max_age=3600)
    config.add_route('index', '/', factory=lambda r: Urns.Admin.Index)
    config.add_route('answers', '/answer', factory=lambda r: Urns.Admin.Answers)
    config.add_route('form', '/form/{form_id}', factory=lambda r: Urns.Admin.Forms)
    config.add_route('forms', '/form', factory=lambda r: Urns.Admin.Forms)
    config.add_route('user', '/user', factory=lambda r: Urns.Admin.User)
    config.add_route('user_permissions', '/permissions', factory=lambda r: Urns.Admin.User)
    config.scan()
    config.set_default_permission(Permissions.Auth)
    config.set_authentication_policy(CookieAuthenticationPolicy())
    config.set_authorization_policy(AuthorizationPolicy())
    """config.add_forbidden_view(lambda r: HTTPTemporaryRedirect('/admin'))"""
    config.add_notfound_view(lambda r: HTTPTemporaryRedirect('/'))
    return config.make_wsgi_app()
