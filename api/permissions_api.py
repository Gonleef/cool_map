from api.permissions_api_v1 import PermissionApiV1
from pyramid.config import Configurator


class PermissionApi(object):
    def __init__(self, config: Configurator):
        config.include(PermissionApiV1, route_prefix='/v1')
