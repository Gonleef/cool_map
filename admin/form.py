from admin import Configuration
from admin.user_loader import load_user
from clients.api_client import ApiClient
from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name='form', renderer='templates/form.jinja2')
class Forms(object):
    def __init__(self, context, request: Request):
        self.context = context
        self.request = request
        self.user = load_user(request)

    def __call__(self):
        form_id = self.request.matchdict.get('form_id')
        form_result = ApiClient(Configuration.get_auth()).form_client.get_form(form_id)
        return {
            'user': self.user,
            'form_result': form_result
        }
