from api.auth_api_v1 import AuthApiV1
from pyramid.config import Configurator


class AuthApi(object):
    def __init__(self, config: Configurator):
        config.include(AuthApiV1, route_prefix='/v1')
