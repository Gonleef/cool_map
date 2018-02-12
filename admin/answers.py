from admin import Configuration
from admin.user_loader import load_user
from clients.api_client import ApiClient
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
        client = ApiClient(Configuration.get_auth())
        answer_result = client.form_client.get_answers(self.request.session.user_id)
        answers = answer_result.data.items if answer_result.is_success else []
        answers = list(map(lambda answer: self.add_form_info(client, answer), answers))
        return {
            'user': self.user,
            'answers': answers
        }

    @staticmethod
    def add_form_info(client: ApiClient, answer: Answer):
        result = client.form_client.get_form(answer.form_id)
        if result.is_success:
            setattr(answer, 'form_info', result.data)
        return answer
