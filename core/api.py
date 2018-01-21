from typing import Callable
from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_defaults

_actions = dict()


@view_defaults(route_name='api')
class Api(object):
    def __init__(self, request: Request):
        self.request = request

    def __call__(self):
        action_name = self.request.matchdict.get('action', None)
        if action_name is not None:
            action_name = action_name.replace('-', '_')
            action_name = self.request.method + '.' + self.__module__ + '.' + action_name
            action = _actions.get(action_name, None)
            if action is not None:
                return action(self)

        response = Response()
        response.status = 400
        return response

    @staticmethod
    def get(action: Callable) -> Callable:
        _actions['GET.' + action.__module__ + '.' + action.__name__] = action
        return action

    @staticmethod
    def post(action: Callable) -> Callable:
        _actions['POST.' + action.__module__ + '.' + action.__name__] = action
        return action
