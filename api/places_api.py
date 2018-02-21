from api.places_api_v1 import PlacesApiV1
from pyramid.config import Configurator


def includeme(config: Configurator):
    config.include(PlacesApiV1, route_prefix='/v1')
