from admin.user_loader import load_user
from clients.api_client import ApiClient
from core.configuration import ConfigurationWrapper
from core.entities import Answer
from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name='answers', renderer='templates/answers.jinja2')
class Answers(object):
    def __init__(self, context, request: Request):
        self.context = context
        self.request = request
        self.user = load_user(request)

    def __call__(self):
        client = ApiClient(ConfigurationWrapper.get_auth('admin'))
        skip = int(self.request.params.get('skip', 0))
        take = int(self.request.params.get('take', 50000))
        answer_result = client.form_client.get_answers(self.request.session.user_id, skip, take)
        if not answer_result.is_success:
            return {
                'user': self.user,
                'error': answer_result.data
            }

        answer_result.data.items = list(map(lambda answer: self.add_form_info(client, answer), answer_result.data.items))
        return {
            'user': self.user,
            'answers': answer_result.data
        }

    @staticmethod
    def add_form_info(client: ApiClient, answer: Answer):
        result = client.form_client.get_form(answer.form_id)
        if result.is_success:
            setattr(answer, 'form_info', result.data)
        return answer
