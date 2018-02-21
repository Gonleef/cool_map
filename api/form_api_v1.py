import json

from api.api import Api, default, route
from api.entities_sql import create_transaction, AnswerSql, FormSql, BindingSql, PlaceSql
from core.entities import ItemsResult, FailResultSimple
from core.http_method import HTTPMethod
from core.response import HTTPOk, HTTPNotFound
from core.urns import Urns
from sqlalchemy.exc import IntegrityError


@default(factory=lambda r: Urns.Api.Forms)
class FormApiV1(Api):
    def __init__(self, *args):
        super(FormApiV1, self).__init__(args)

    @route(HTTPMethod.GET, 'form/{id}')
    def get_form(self):
        id = self.request.matchdict.get('id')
        with create_transaction() as transaction:
            form = transaction.query(FormSql) \
                .filter(FormSql.id == id) \
                .first()
            return HTTPOk(form.val()) if form \
                else HTTPNotFound(FailResultSimple('FormNotFound', 'Форма не найдена'))

    @route(HTTPMethod.DELETE, 'form/{id}')
    def delete_form(self):
        id = self.request.matchdict.get('id')
        with create_transaction() as transaction:
            deleted = transaction.query(FormSql) \
                .filter(FormSql.id == id) \
                .delete()
            transaction.query(AnswerSql) \
                .filter(AnswerSql.form_id == id) \
                .delete()
            return HTTPOk() if deleted \
                else HTTPNotFound(FailResultSimple('FormNotFound', 'Форма не найдена'))

    @route(HTTPMethod.POST, 'form/{id}')
    def set_form(self):
        id = self.request.matchdict.get('id')
        data = self.request.body.decode()
        data = json.loads(data)
        with create_transaction() as transaction:
            patched = transaction.query(FormSql) \
                .filter(FormSql.id == id) \
                .update(data)
            return HTTPOk() if patched \
                else HTTPNotFound(FailResultSimple('FormNotFound', 'Форма не найдена'))

    @route(HTTPMethod.PUT, 'form/{id}')
    def put_form(self):
        id = self.request.matchdict.get('id')
        data = self.request.body.decode()
        data = json.loads(data)
        form = FormSql(id=id, **data)
        try:
            with create_transaction() as transaction:
                transaction.add(form)
            return HTTPOk()
        except IntegrityError:
            return HTTPNotFound(FailResultSimple('FormNotCreated', 'Форма не создана'))

    @route(HTTPMethod.GET, 'user/{user_id}/form')
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

    @route(HTTPMethod.GET, 'answer/{id}')
    def get_answer(self):
        id = self.request.matchdict.get('id')
        with create_transaction() as transaction:
            answer = transaction.query(AnswerSql) \
                .filter(AnswerSql.id == id) \
                .first()
            return HTTPOk(answer.val()) if answer \
                else HTTPNotFound(FailResultSimple('AnswerNotFound', 'Ответ не найдена'))

    @route(HTTPMethod.DELETE, 'answer/{id}')
    def delete_answer(self):
        id = self.request.matchdict.get('id')
        with create_transaction() as transaction:
            deleted = transaction.query(AnswerSql) \
                .filter(AnswerSql.id == id) \
                .delete()
            return HTTPOk() if deleted \
                else HTTPNotFound(FailResultSimple('AnswerNotFound', 'Ответ не найдена'))

    @route(HTTPMethod.POST, 'answer/{id}')
    def set_answer(self):
        id = self.request.matchdict.get('id')
        answer = self.request.body.decode()
        with create_transaction() as transaction:
            patched = transaction.query(AnswerSql) \
                .filter(AnswerSql.id == id) \
                .update({AnswerSql.answer: answer})
            return HTTPOk() if patched \
                else HTTPNotFound(FailResultSimple('AnswerNotFound', 'Ответ не найдена'))

    @route(HTTPMethod.GET, 'user/{user_id}/answer')
    def get_answers(self):
        user_id = self.request.matchdict.get('user_id')
        skip = int(self.request.matchdict.get('skip', 0))
        take = int(self.request.matchdict.get('take', 50000))

        with create_transaction() as transaction:
            count = transaction.query(AnswerSql) \
                .filter(AnswerSql.respondent_id == user_id) \
                .count()

            if count == 0 or skip >= count:
                return HTTPNotFound(ItemsResult([], skip, take, count))

            answers = transaction.query(AnswerSql) \
                          .filter(AnswerSql.respondent_id == user_id) \
                [skip:take]
            items = list(map(lambda p: p.val().__dict__, answers))
            return HTTPOk(ItemsResult(items, skip, take, count))

    @route(HTTPMethod.GET, 'form/{form_id}/bindings')
    def get_places(self):
        form_id = self.request.matchdict.get('form_id')
        skip = int(self.request.matchdict.get('skip', 0))
        take = int(self.request.matchdict.get('take', 50000))
        with create_transaction() as transaction:
            count = transaction.query(BindingSql) \
                .join(PlaceSql, BindingSql.place_id == PlaceSql.id) \
                .filter(BindingSql.form_id == form_id) \
                .count()
            if count == 0 or skip >= count:
                return HTTPNotFound(ItemsResult([], skip, take, count))
            answers = transaction.query(PlaceSql) \
                          .join(BindingSql, BindingSql.place_id == PlaceSql.id) \
                          .filter(BindingSql.form_id == form_id) \
                [skip:take]
            items = list(map(lambda p: p.val().__dict__, answers))
            return HTTPOk(ItemsResult(items, skip, take, count))

    @route(HTTPMethod.DELETE, 'form/{form_id}/place/{place_id}')
    def delete_binding(self):
        form_id = self.request.matchdict.get('form_id')
        place_id = self.request.matchdict.get('place_id')
        with create_transaction() as transaction:
            deleted = transaction.query(BindingSql) \
                .filter(BindingSql.form_id == form_id and BindingSql.place_id == place_id) \
                .delete()
            return HTTPOk() if deleted \
                else HTTPNotFound(FailResultSimple('BindingNotFound', 'Привязка не найдена'))

    @route(HTTPMethod.PUT, 'form/{form_id}/place/{place_id}')
    def add_binding(self):
        form_id = self.request.matchdict.get('form_id')
        place_id = self.request.matchdict.get('place_id')
        with create_transaction() as transaction:
            binding = BindingSql(form_id, place_id)
            transaction.add(binding)
            return HTTPOk()
