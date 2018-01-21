from pyramid.config import Configurator


def get_app(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('api', '/{version}/{action}')
    config.scan('core.base_api_configuration')
    config.scan()
    return config.make_wsgi_app()
