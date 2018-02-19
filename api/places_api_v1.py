from http import HTTPStatus

from api.api import Api, default, route
from core.configuration import ConfigurationWrapper
from core.entities import FailResultSimple
from core.http_headers import HTTPHeaders
from core.http_method import HTTPMethod
from core.response import HTTPOk, HTTPBadResponse
from core.urns import Urns
from pyramid.request import Request

"""
Nominatim Usage Policy
https://operations.osmfoundation.org/policies/nominatim/
"""


@default(factory=lambda r: Urns.Api.Users)
class PlacesApiV1(Api):
    def __init__(self, *args):
        super(PlacesApiV1, self).__init__(args)

    @route(HTTPMethod.GET, 'geodecoding')
    def put(self):
        latitude = self.request.params.get('lat')
        longitude = self.request.params.get('lon')
        nominatim = ConfigurationWrapper.instance('api').get('nominatim')
        request = Request.blank(nominatim + '/reverse?format=json&lat=%s&lon=%s&addressdetails=1' % (latitude, longitude))
        request.user_agent = 'CoolMap/1.0.0'
        response = request.get_response()
        if response.status_code != HTTPStatus.OK.value:
            return HTTPBadResponse(FailResultSimple('FailGeodecoding', 'Fail to geodecoding'))
        data = response.json_body
        osm_type = data.get('osm_type')[0].upper()
        osm_id = data.get('osm_id')
        id = osm_type + osm_id
        address = data.get('address')
        display = data.get('display_name')
        return HTTPOk()

    def _update_place(self, id: str, display: str, address: dict):
        pass
