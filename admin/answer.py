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
        if self.request.method == HTTPMethod.POST.value:
            return self.edit()
        elif self.request.method == HTTPMethod.DELETE.value:
            return self.delete()
        elif self.request.params.get('delete') == 'true':
            return self.delete()
        return self.get()

    def get(self, success: str = None):
        client = ApiClient(ConfigurationWrapper.get_auth('admin'))
        answer_id = self.request.matchdict.get('answer_id')
        answer_result = client.form_client.get_answer(answer_id)
        if not answer_result.is_success:
            return {
                'user': self.user,
                'error': answer_result.data
            }
        form_result = client.form_client.get_form(answer_result.data.form_id)
        if not form_result.is_success:
            return {
                'user': self.user,
                'error': form_result.data
            }
        inputs = json.loads(form_result.data.content)
        answers = json.loads(answer_result.data.answer)
        for input_id in inputs:
            label = inputs[input_id]
            inputs[input_id] = {
                'label': label,
                'answer': answers.get(input_id, '')
            }
        return {
            'success': success,
            'user': self.user,
            'answer_id': answer_id,
            'form': form_result.data,
            'inputs': inputs
        }

    def delete(self):
        answer_id = self.request.matchdict.get('answer_id')
        result = ApiClient(ConfigurationWrapper.get_auth('admin')).form_client.delete_answer(answer_id)
        if not result.is_success:
            logging.warning("Fail to delete answer '%s': %s" % (answer_id, result.data.message))
        return HTTPTemporaryRedirect('/admin/answer')

    def edit(self):
        answer_id = self.request.matchdict.get('answer_id')
        answer = dict()
        for id in self.request.params:
            answer[id] = self.request.params[id]
        answer = json.dumps(answer)
        result = ApiClient(ConfigurationWrapper.get_auth('admin')).form_client.set_answer(answer_id, answer)
        if not result.is_success:
            return {
                'user': self.user,
                'error': result.data
            }
        return self.get('Новый ответ записан')
