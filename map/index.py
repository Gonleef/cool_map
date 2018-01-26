from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name='index', renderer='templates/map.jinja2')
def index(req: Request):
    return {}
