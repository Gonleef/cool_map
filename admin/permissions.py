from admin.user_loader import load_user
from clients.api_client import ApiClient
from core.configuration import ConfigurationWrapper
from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name='user_permissions', renderer='templates/permissions.jinja2')
class Permissions(object):
    def __init__(self, context, request: Request):
        self.request = request
        self.context = context
        self.user = load_user(request)

    def __call__(self):
        client = ApiClient(ConfigurationWrapper.get_auth())
        skip = int(self.request.params.get('skip', 0))
        take = int(self.request.params.get('take', 50000))
        result = client.permission_client.get_permissions(skip, take)
        if not result.is_success:
            raise Exception(result.data)

        return {
            'user': self.user,
            'permissions': result.data
        }
