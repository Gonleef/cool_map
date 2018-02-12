from api.users_api_v1 import UsersApiV1
from pyramid.config import Configurator


class UsersApi(object):
    def __init__(self, config: Configurator):
        config.include(UsersApiV1, route_prefix='/v1')
