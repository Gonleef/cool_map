from pyramid.view import view_config
from pyramid.response import Response


@view_config(route_name='index', request_method='GET')
def auth_index(request):
    return Response('OK_OLOLOLO')
