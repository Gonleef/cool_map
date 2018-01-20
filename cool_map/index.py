from pyramid.view import view_config


@view_config(route_name='index', renderer='templates/popups.jinja2')
def index(requests):
    return {}
