from pyramid.view import view_config


@view_config(route_name='index', renderer='templates/map.jinja2')
def index(req):
    return {}
