from admin.user_loader import load_user
from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name='user_permissions', renderer='templates/permissions.jinja2')
class Permissions(object):
    def __init__(self, context, request: Request):
        self.request = request
        self.context = context
        self.user = load_user(request)

    def __call__(self):
        return {
            'user': self.user,
        }
