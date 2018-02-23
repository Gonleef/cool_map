import json
from http import HTTPStatus

from api.api import Api, default, route
from api.entities_sql import create_transaction, BindingSql, PlaceSql, FormSql
from core.configuration import ConfigurationWrapper
from core.entities import FailResultSimple, ItemsResult
from core.http_headers import HTTPHeaders
from core.http_method import HTTPMethod
from core.permissions import Permissions
from core.response import HTTPOk, HTTPBadResponse, HTTPNotFound
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

    @route(HTTPMethod.GET, 'geodecoding', permission=Permissions.Null)
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
        title = data.get('display_name')
        address = json.dumps(data.get('address'))
        place = self._add_or_update(osm_id, osm_type, address, title)
        return HTTPOk(place)

    @route(HTTPMethod.GET, 'get/{id}')
    def get_by_id(self):
        pass

    @route(HTTPMethod.GET, 'get/osm/{id}')
    def get_by_id(self):
        pass

    def _add_or_update(self, osm_id: int, osm_type: str, address: str, title: str):
        with create_transaction() as transaction:
            place = transaction.query(PlaceSql) \
                .filter(PlaceSql.osm_id == osm_id and PlaceSql.osm_type == osm_type) \
                .first()
            if place:
                transaction.query(PlaceSql)\
                    .filter(PlaceSql.id == place.id)\
                    .update({PlaceSql.address: address, PlaceSql.title: title})
                place = place.val()
                place.title = title
                place.address = address
            else:
                place = PlaceSql(osm_type, osm_id, title, address)
                transaction.add(place)
                place = place.val()
            return place
