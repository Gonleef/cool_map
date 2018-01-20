from pyramid.config import Configurator
from auth.not_found import not_found_view


def get_app(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('index', '/')
    config.add_notfound_view(not_found_view)
    config.scan()
    return config.make_wsgi_app()
