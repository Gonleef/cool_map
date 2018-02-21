import uuid

from admin.user_loader import load_user
from clients.api_client import ApiClient
from core.configuration import ConfigurationWrapper
from core.response import HTTPOkWithRedirect
from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name='binding', renderer='templates/binding.jinja2')
class BindingsPage(object):
    def __init__(self, context, request: Request):
        self.request = request
        self.context = context
        self.user = load_user(request)

    def __call__(self):
        if self.request.params.get('delete', '').lower() == 'true':
            return self.delete()
        elif self.request.params.get('create', '').lower() == 'true':
            return self.create()
        return self.add()

    def delete(self):
        client = ApiClient(ConfigurationWrapper.get_auth('admin'))
        form_id = self.request.matchdict.get('form_id')
        place_id = self.request.matchdict.get('place_id')
        result = client.form_client.delete_binding(form_id, place_id)
        if not result.is_success:
            return {
                'error': result.data,
                'user': self.user
            }
        return HTTPOkWithRedirect('/admin/form/%s/place' % form_id)

    def create(self):
        client = ApiClient(ConfigurationWrapper.get_auth('admin'))
        form_id = self.request.matchdict.get('form_id')
        place_id = self.request.matchdict.get('place_id')
        result = client.form_client.create_binding(form_id, place_id)
        if not result.is_success:
            return {
                'error': result.data,
                'user': self.user
            }
        return HTTPOkWithRedirect('/admin/form/%s/place' % form_id)

    def add(self):
        form_id = self.request.matchdict.get('form_id')
        return {
            'form_id': form_id,
            'user': self.user
        }
