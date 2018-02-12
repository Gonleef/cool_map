from admin import Configuration
from admin.user_loader import load_user
from clients.api_client import ApiClient
from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name='forms', renderer='templates/forms.jinja2')
class Forms(object):
    def __init__(self, context, request: Request):
        self.request = request
        self.context = context
        self.user = load_user(request)

    def __call__(self):
        forms_result = ApiClient(Configuration.get_auth()).form_client.get_forms(self.request.session.user_id)
        forms = forms_result.data.items if forms_result.is_success else []
        return {
            'user': self.user,
            'forms': forms
        }