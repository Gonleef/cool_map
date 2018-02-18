from api.auth_api_v1 import AuthApiV1
from pyramid.config import Configurator


def includeme(config: Configurator):
    config.include(AuthApiV1, route_prefix='/v1')
