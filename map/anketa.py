import json
from http import HTTPStatus

from clients.api_client import ApiClient
from core.configuration import ConfigurationWrapper
from core.http_method import HTTPMethod
from core.permissions import Permissions
from core.response import HTTPOkWithRedirect
from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config
from admin.user_loader import load_user

@view_config(route_name='anketa', renderer='templates/anketa.jinja2', permission=Permissions.Null)
def index(req: Request):
    client = ApiClient(ConfigurationWrapper.get_auth("map"));
    form = client.form_client.get_form(req.params.get("id"))
    place_id = client.form_client.get_form(req.params.get("place_id"))
    return { 'inputs': json.loads(form.data.content), 'place_id': place_id, 'form_id': req.params.get("id")}

@view_config(route_name='xXx_PRO100anketka228_xXx', permission=Permissions.Null)
def index_228(req: Request):
    client = ApiClient(ConfigurationWrapper.get_auth("map"));
    user = load_user(req)
    ids = user.id if user else \
        "00000000-0000-0000-0000--000000000000"

    answer = dict()
    for id in req.params:
        answer[id] = req.params[id]
    form_id = answer.pop("form_id")
    place_id = answer.pop("place_id")
    answer = json.dumps(answer)
    form = client.form_client.create_answer(ids, form_id, place_id, answer)
    return HTTPOkWithRedirect("/")
