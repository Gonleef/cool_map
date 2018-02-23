import json
import logging

from admin.user_loader import load_user
from clients.api_client import ApiClient
from core.configuration import ConfigurationWrapper
from core.http_method import HTTPMethod
from core.response import HTTPTemporaryRedirect, HTTPOkWithRedirect
from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name='form', renderer='templates/form.jinja2')
class FormPage(object):
    def __init__(self, context, request: Request):
        self.context = context
        self.request = request
        self.user = load_user(request)

    def __call__(self):
        if self.request.method == HTTPMethod.POST.value:
            return self.edit()
        elif self.request.method == HTTPMethod.DELETE.value:
            return self.delete()
        elif self.request.method == HTTPMethod.PUT.value:
            return self.delete()
        if self.request.params.get('delete', '').lower() == 'true':
            return self.delete()
        if self.request.params.get('create', '').lower() == 'true':
            return self.put()
        return self.get()

    def get(self, success=None):
        form_id = self.request.matchdict.get('form_id')
        form_result = ApiClient(ConfigurationWrapper.get_auth('admin')).form_client.get_form(form_id)
        if not form_result.is_success:
            return {
                'user': self.user,
                'error': form_result.data
            }

        inputs = json.loads(form_result.data.content)
        return {
            'success': success,
            'user': self.user,
            'form': form_result.data,
            'inputs': inputs
        }

    def delete(self):
        form_id = self.request.matchdict.get('form_id')
        result = ApiClient(ConfigurationWrapper.get_auth('admin')).form_client.delete_form(form_id)
        if not result.is_success:
            logging.warning("Fail to delete form '%s': %s" % (form_id, result.data.message))
        return HTTPOkWithRedirect('/admin/form')

    def edit(self):
        form_id = self.request.matchdict.get('form_id')
        answer = dict()
        for id in self.request.params:
            answer[id] = self.request.params[id]
        title = answer.pop('title')
        description = answer.pop('description')
        content = json.dumps(answer)
        result = ApiClient(ConfigurationWrapper.get_auth('admin')).form_client.set_form(form_id, title, description, content)
        if not result.is_success:
            return {
                'user': self.user,
                'error': result.data
            }
        return self.get('Формы поправлена')

    def put(self):
        form_id = self.request.matchdict.get('form_id')
        result = ApiClient(ConfigurationWrapper.get_auth('admin')).form_client.create_form(self.user.id, id=form_id)
        if not result.is_success:
            return {
                'user': self.user,
                'error': result.data
            }
        return HTTPOkWithRedirect('/admin/form/' + form_id)
