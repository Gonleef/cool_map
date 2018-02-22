from api.api import Api, default, route
from api.entities_sql import UserSql, create_transaction
from core.entities import FailResultSimple
from core.http_method import HTTPMethod
from core.response import HTTPOk, HTTPNotFound, HTTPBadResponse
from core.urns import Urns
from sqlalchemy.exc import IntegrityError


@default(factory=lambda r: Urns.Api.Users)
class UsersApiV1(Api):
    def __init__(self, *args):
        super(UsersApiV1, self).__init__(args)

    @route(HTTPMethod.PUT, 'user')
    def put(self):
        login = self.request.params.get('login')
        email = self.request.params.get('email')
        password = self.request.body.decode()
        try:
            with create_transaction() as transaction:
                user = UserSql(login, password, email)
                transaction.add(user)
                return HTTPOk(user.id)
        except IntegrityError:
            return HTTPBadResponse(FailResultSimple("FailRegister", "Не удалось зарегистрировать"))

    @route(HTTPMethod.GET, 'user/{user_id}')
    def get(self):
        user_id = self.request.matchdict.get('user_id')
        with create_transaction() as transaction:
            state = transaction.query(UserSql).filter(UserSql.id == user_id).first()
            return HTTPOk(state.val()) if state is not None \
                else HTTPNotFound(FailResultSimple("UserNotFound", "Пользователь не найдена"))
