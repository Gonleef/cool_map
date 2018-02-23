from http import HTTPStatus

from clients.api_client import ApiClient
from core.configuration import ConfigurationWrapper
from core.http_method import HTTPMethod
from core.permissions import Permissions
from core.response import HTTPOkWithRedirect
from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='choose', renderer='templates/choose.jinja2', permission=Permissions.Null)
def index(req: Request):
    client = ApiClient(ConfigurationWrapper.get_auth("map"));
    #print(req.params.get("place_id"))
    forms = client.form_client.get_forms_place_id(req.params.get("place_id"))
    return { 'forms': forms.data.items, 'place_id': req.params.get("place_id") }
