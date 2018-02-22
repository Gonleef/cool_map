from clients.api_client import ApiClient
from core.configuration import ConfigurationWrapper
from core.http_method import HTTPMethod
from core.permissions import Permissions
from core.response import HTTPOkWithRedirect
from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name='registration', renderer='templates/registration.jinja2', permission=Permissions.Null)
class Enter(object):
    def __init__(self, context, request: Request):
        self.request = request
        self.context = context

    def __call__(self):
        if self.request.method == HTTPMethod.POST.value:
            return self.register()
        return {}

    def register(self):
        login = self.request.params.get('login')
        email = self.request.params.get('email')
        new_password1 = self.request.params.get('new_password1')
        new_password2 = self.request.params.get('new_password2')
        if new_password1 != new_password2:
            return {
                'error': 'Пароли не совпадают'
            }
        client = ApiClient(ConfigurationWrapper.get_auth('map'))
        result = client.users_client.create(login, new_password1, email)
        if not result.is_success:
            return {
                'error': 'Логин занят'
            }
        return HTTPOkWithRedirect('/enter')
