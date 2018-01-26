from core.response import HTTPTemporaryRedirect
from pyramid.config import Configurator


def get_app(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('core_static', 'core:static', cache_max_age=3600)
    config.add_route('index', '/')
    config.scan()
    config.add_notfound_view(lambda r: HTTPTemporaryRedirect('/'))
    return config.make_wsgi_app()
