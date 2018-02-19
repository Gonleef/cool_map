import uuid

from admin.user_loader import load_user
from clients.api_client import ApiClient
from core.configuration import ConfigurationWrapper
from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name='bindings', renderer='templates/bindings.jinja2')
class PlacesPage(object):
    def __init__(self, context, request: Request):
        self.request = request
        self.context = context
        self.user = load_user(request)

    def __call__(self):
        client = ApiClient(ConfigurationWrapper.get_auth('admin'))
        form_id = self.request.matchdict.get('form_id')
        skip = int(self.request.params.get('skip', 0))
        take = int(self.request.params.get('take', 50000))
        bindings_result = client.form_client.get_bindings(form_id, skip, take)
        if not bindings_result.is_success:
            return {
                'user': self.user,
                'error': bindings_result.data
            }

        return {
            'user': self.user,
            'places': bindings_result.data,
            'random_uuid': str(uuid.uuid4())
        }
