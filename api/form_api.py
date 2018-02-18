from api.form_api_v1 import FormApiV1
from pyramid.config import Configurator


def includeme(config: Configurator):
    config.include(FormApiV1, route_prefix='/v1')
