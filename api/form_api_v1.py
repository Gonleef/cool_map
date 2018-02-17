from api.api import Api, default, route
from core.entities import ItemsResult, FailResultSimple
from core.entities_sql import create_transaction, AnswerSql, FormSql
from core.http_method import HTTPMethod
from core.response import HTTPOk, HTTPNotFound
from core.urns import Urns


@default(factory=lambda r: Urns.Api.Forms)
class FormApiV1(Api):
    def __init__(self, *args):
        super(FormApiV1, self).__init__(args)

    @route(HTTPMethod.GET, 'form/{form_id}')
    def get_form(self):
        print(1)
        form_id = self.request.matchdict.get('form_id')
        with create_transaction() as transaction:
            form = transaction.query(FormSql) \
                .filter(FormSql.id == form_id) \
                .first()
            return HTTPOk(form.val()) if form \
                else HTTPNotFound(FailResultSimple('FormNotFound', 'Форма не найдена'))

    @route(HTTPMethod.DELETE, 'form/{form_id}')
    def delete_form(self):
        form_id = self.request.matchdict.get('form_id')
        with create_transaction() as transaction:
            deleted = transaction.query(FormSql) \
                .filter(FormSql.id == form_id) \
                .delete()
            transaction.query(AnswerSql) \
                .filter(AnswerSql.form_id == form_id) \
                .delete()
            return HTTPOk() if deleted \
                else HTTPNotFound(FailResultSimple('FormNotFound', 'Форма не найдена'))

    @route(HTTPMethod.GET, 'forms/for/{user_id}')
    def get_forms(self):
        user_id = self.request.matchdict.get('user_id')
        skip = int(self.request.matchdict.get('skip', 0))
        take = int(self.request.matchdict.get('take', 50000))

        with create_transaction() as transaction:
            count = transaction.query(FormSql)\
                .filter(FormSql.creator == user_id)\
                .count()

            if count == 0 or skip >= count:
                return HTTPNotFound(ItemsResult([], skip, take, count))

            answers = transaction.query(FormSql)\
                .filter(FormSql.creator == user_id)\
                [skip:take]
            items = list(map(lambda p: p.val().__dict__, answers))
            return HTTPOk(ItemsResult(items, skip, take, count))

    @route(HTTPMethod.GET, 'answers/for/{user_id}')
    def answer(self):
        user_id = self.request.matchdict.get('user_id')
        skip = int(self.request.matchdict.get('skip', 0))
        take = int(self.request.matchdict.get('take', 50000))

        with create_transaction() as transaction:
            count = transaction.query(AnswerSql)\
                .filter(AnswerSql.respondent_id == user_id)\
                .count()

            if count == 0 or skip >= count:
                return HTTPNotFound(ItemsResult([], skip, take, count))

            answers = transaction.query(AnswerSql)\
                .filter(AnswerSql.respondent_id == user_id)\
                [skip:take]
            items = list(map(lambda p: p.val().__dict__, answers))
            return HTTPOk(ItemsResult(items, skip, take, count))
