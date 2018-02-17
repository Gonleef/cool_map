from http import HTTPStatus

from clients.api_client import ApiClient
from core.configuration import ConfigurationWrapper
from core.http_method import HTTPMethod
from core.permissions import Permissions
from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='enter', renderer='templates/enter.jinja2', permission=Permissions.Null)
class Enter(object):
    def __init__(self, context, request: Request):
        self.request = request
        self.context = context

    def __call__(self):
        if self.request.auth_sid:
            return self.redirect()
        elif self.request.method == HTTPMethod.POST.value:
            return self.enter()

        return {}

    def enter(self):
        login = self.request.params.get('login', '')
        password = self.request.params.get('password', '')
        remember = self.request.params.get('remember')
        result = ApiClient(ConfigurationWrapper.get_auth()).auth_client.authenticate_by_pass(login, password, self.request.client_addr)
        if not result.is_success:
            return {'result': result.data}

        max_age = 30 * 24 * 60 * 60 if remember else None
        return self.redirect(lambda r: r.set_cookie('auth.sid', result.data, httponly=True, max_age=max_age))

    def redirect(self, response_wrapper=lambda r: None):
        back_url = self.request.params.get('back_url', '/')

        response = Response()
        response.status = HTTPStatus.OK
        response.location = back_url
        response_wrapper(response)
        response.body = ('<script>location.href = "' + back_url + '"</script>').encode()
        return response
