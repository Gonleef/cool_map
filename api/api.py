import sys
from typing import Callable, Any
from core.http_method import HTTPMethod
from pyramid.config import Configurator
from pyramid.request import Request


ATTR_ADD_ROUTES = '__add_routes__'
ATTR_DEPTH = '__depth__'


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


def default(**settings):
    def decorator(wrapped):
        wrapped.__init__.__dict__.update(settings)
        return wrapped
    return decorator


def route(
        method: HTTPMethod,
        pattern: str = None,
        auto_pattern: bool = True,
        auto_pattern_prefix: str = '/',
        auto_pattern_suffix: str = '',
        **settings):
    def decorator(wrapped):
        _pattern = pattern if not auto_pattern else auto_pattern_prefix + wrapped.__name__ + auto_pattern_suffix
        return _route(method, _pattern, settings)(wrapped)
    return decorator


def route(method: HTTPMethod, pattern: str, **settings):
    return _route(method, pattern, settings)


def action(method: HTTPMethod, prefix: str = '/', suffix: str = '', **settings):
    def decorator(wrapped):
        settings[ATTR_DEPTH] = 1
        pattern = prefix + wrapped.__name__ + suffix
        return _route(method, pattern, settings)(wrapped)
    return decorator


def post(pattern: str, **settings):
    return route(HTTPMethod.POST, pattern, **settings)


def get(pattern: str, **settings):
    return route(HTTPMethod.GET, pattern, **settings)


def action_post(prefix: str = '/', suffix: str = '', **settings):
    return action(HTTPMethod.POST, prefix, suffix, **settings)


def action_get(prefix: str = '/', suffix: str = '', **settings):
    return action(HTTPMethod.GET, prefix, suffix, **settings)


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
        route_name = None if pattern is None else view.__qualname__ + '.' + str(pattern.__hash__())
        route_name = settings.get('route_name', route_name)
        settings['route_name'] = route_name
        if pattern is not None:
            config.add_route(route_name, pattern, factory=factory)
        config.add_view(self.__class__, **settings)
