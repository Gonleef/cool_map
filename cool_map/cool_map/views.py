from pyramid.view import view_config
from pyramid.request import Request


@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'cool_map'}
