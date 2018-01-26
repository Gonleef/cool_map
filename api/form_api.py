from api.form_api_v1 import FormApiV1
from pyramid.config import Configurator


class FormApi(object):
    def __init__(self, config: Configurator):
        config.include(FormApiV1, route_prefix='/v1')
