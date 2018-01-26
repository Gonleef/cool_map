from admin import Configuration
from clients.auth_provider import SessionAuthProvider
from clients.form_client_v1 import FormClient
from core.entities import Answer
from core.permissions import Permissions
from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name='create', renderer='templates/create.jinja2', permission=Permissions.Create)
class Create(object):
    _auth = SessionAuthProvider(Configuration.Sid)

    def __init__(self, context, request: Request):
        self.request = request
        self.context = context

    def __call__(self):
        return {}
