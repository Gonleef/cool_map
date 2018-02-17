import json
import logging

from admin.user_loader import load_user
from clients.api_client import ApiClient
from core.configuration import ConfigurationWrapper
from core.http_method import HTTPMethod
from core.response import HTTPTemporaryRedirect
from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name='answer', renderer='templates/answer.jinja2')
class Form(object):
    def __init__(self, context, request: Request):
        self.context = context
        self.request = request
        self.user = load_user(request)

    def __call__(self):
        if self.request.method == HTTPMethod.GET.value:
            if self.request.params.get('delete') == 'true':
                return self.delete()

            return self.edit()
        elif self.request.method == HTTPMethod.DELETE.value:
            return self.delete()

    def edit(self):
        form_id = self.request.matchdict.get('answer_id')
        form_result = ApiClient(ConfigurationWrapper.get_auth()).form_client.get_form(form_id)
        if not form_result.is_success:
            return {
                'user': self.user,
                'error': form_result.data
            }

        inputs = json.loads(form_result.data.content)
        print(inputs)
        return {
            'user': self.user,
            'form': form_result.data,
            'inputs': inputs
        }

    def delete(self):
        form_id = self.request.matchdict.get('answer_id')
        result = ApiClient(ConfigurationWrapper.get_auth()).form_client.delete_form(form_id)
        if not result.is_success:
            logging.warning("Fail to delete form '%s': %s" % (form_id, result.data.message))
        return HTTPTemporaryRedirect('/admin/answer')


