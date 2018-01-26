from api.api import Api, action_get, get, default
from core.entities import ItemsResult, FailResult
from core.entities_sql import create_transaction, AnswerSql, FormSql
from core.response import HTTPOk, HTTPNotFound


@default(factory=lambda r: 'global:form')
class FormApiV1(Api):
    def __init__(self, *args):
        super(FormApiV1, self).__init__(args)

    @get('form/{form_id}')
    def get_form(self):
        form_id = self.request.matchdict.get('form_id')
        with create_transaction() as transaction:
            form = transaction.query(FormSql) \
                .filter(FormSql.id == form_id) \
                .first()
            return HTTPOk(form.val()) if form is not None \
                else HTTPNotFound(FailResult('FormNotFound', 'Форма не найдена'))

    @get('forms/for/{user_id}')
    def get_forms(self):
        user_id = self.request.matchdict.get('user_id')
        skip = int(self.request.matchdict.get('skip', 0))
        take = int(self.request.matchdict.get('take', 50000))

        with create_transaction() as transaction:
            count = transaction.query(FormSql)\
                .filter(FormSql.creator == user_id)\
                .count()

            if count == 0 or skip >= count:
                return HTTPNotFound(items=[], skip=skip, take=take, count=count)

            answers = transaction.query(FormSql)\
                .filter(FormSql.creator == user_id)\
                [skip:take]
            items = list(map(lambda p: p.val().__dict__, answers))
            return HTTPOk(ItemsResult(items, skip, take, count))

    @get('answers/for/{user_id}')
    def answer(self):
        user_id = self.request.matchdict.get('user_id')
        skip = int(self.request.matchdict.get('skip', 0))
        take = int(self.request.matchdict.get('take', 50000))

        with create_transaction() as transaction:
            count = transaction.query(AnswerSql)\
                .filter(AnswerSql.respondent_id == user_id)\
                .count()

            if count == 0 or skip >= count:
                return HTTPNotFound(items=[], skip=skip, take=take, count=count)

            answers = transaction.query(AnswerSql)\
                .filter(AnswerSql.respondent_id == user_id)\
                [skip:take]
            items = list(map(lambda p: p.val().__dict__, answers))
            return HTTPOk(ItemsResult(items, skip, take, count))
