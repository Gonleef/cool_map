from http import HTTPStatus

from core.permissions import Permissions
from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config


@view_config(route_name='exit', permission=Permissions.Null)
class Exit(object):
    def __init__(self, context, request: Request):
        self.request = request
        self.context = context

    def __call__(self):
        back_url = self.request.params.get('back_url', '/')

        response = Response()
        response.status = HTTPStatus.OK
        response.location = back_url
        response.delete_cookie('auth.sid')
        response.body = ('<script>location.href = "' + back_url + '"</script>').encode()
        return response
