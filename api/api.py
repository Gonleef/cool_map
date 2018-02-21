import sys
from typing import Callable, Any
from core.http_method import HTTPMethod
from pyramid.config import Configurator
from pyramid.request import Request


ATTR_ADD_ROUTES = '__add_routes__'
ATTR_DEPTH = '__depth__'


def default(**settings):
    def decorator(wrapped):
        wrapped.__init__.__dict__.update(settings)
        return wrapped
    return decorator


def _route(method: HTTPMethod, pattern: str, settings):
    def decorator(wrapped):
        depth = settings.pop(ATTR_DEPTH, 0)
        init = sys._getframe(depth+1).f_locals.get('__init__')
        if ATTR_ADD_ROUTES not in init.__dict__:
            init.__dict__[ATTR_ADD_ROUTES] = []
        init.__dict__[ATTR_ADD_ROUTES].append(wrapped)
        wrapped.__dict__['pattern'] = pattern
        wrapped.__dict__['request_method'] = method.value
        wrapped.__dict__['attr'] = wrapped.__name__
        wrapped.__dict__.update(settings)
        return wrapped
    return decorator


def route(method: HTTPMethod, pattern: str, **settings):
    return _route(method, pattern, settings)


def autoroute(method: HTTPMethod, prefix: str = '/', suffix: str = '', **settings):
    def decorator(wrapped):
        settings[ATTR_DEPTH] = 1
        pattern = prefix + wrapped.__name__ + suffix
        return _route(method, pattern, settings)(wrapped)
    return decorator


class Api(object):
    context: Any
    request: Request

    def __init__(self, args):
        if len(args) < 1 or len(args) > 2:
            raise EnvironmentError()
        if isinstance(args[0], Configurator):
            routes = self.__init__.__dict__.pop(ATTR_ADD_ROUTES, [])
            for route in routes:
                self._add_route(args[0], route, self.__init__.__dict__.copy())
        else:
            self.context = args[0]
            self.request = args[1]

    def _add_route(self, config: Configurator, view: Callable, settings: dict):
        settings.update(view.__dict__)
        pattern = settings.pop('pattern', None)
        factory = settings.pop('factory', None)
        method = settings.pop('request_method', HTTPMethod.GET.value)
        route_name = method + '_' + pattern
        route_name = settings.get('route_name', route_name)
        settings['route_name'] = route_name
        if pattern is not None:
            config.add_route(route_name, pattern, factory=factory, request_method=method)
        config.add_view(self.__class__, **settings)
