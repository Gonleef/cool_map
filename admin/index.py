from admin.user_loader import load_user
from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name='index', renderer='templates/index.jinja2')
class IndexPage(object):
    def __init__(self, context, request: Request):
        self.context = context
        self.request = request
        self.user = load_user(request)

    def __call__(self):
        return {
            'user': self.user,
        }
