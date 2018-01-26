from admin import Configuration
from clients.auth_provider import SessionAuthProvider
from clients.form_client_v1 import FormClient
from core.entities import Answer
from pyramid.request import Request
from pyramid.view import view_config


@view_config(route_name='index', renderer='templates/index.jinja2')
class Index(object):
    _auth = SessionAuthProvider(Configuration.Sid)

    def __init__(self, context, request: Request):
        self.request = request
        self.context = context

    def __call__(self):
        form_client = FormClient(self._auth)
        answer_result = form_client.get_answers(self.request.session.user_id)
        answers = answer_result.data.items if answer_result.is_success else []

        def add_form_info(answer: Answer):
            result = form_client.get_form(answer.form_id)
            if result.is_success:
                setattr(answer, 'form_info', result.data)
            return answer

        answers = list(map(add_form_info, answers))
        forms_result = form_client.get_forms(self.request.session.user_id)
        forms = forms_result.data.items if forms_result.is_success else []
        return {
            'answer': answers,
            'forms': forms
        }
