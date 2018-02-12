from api.api import Api, default, put, get
from core.entities import FailResult
from core.entities_sql import UserSql, create_transaction
from core.response import HTTPOk, HTTPNotFound
from core.urns import Urns


@default(factory=lambda r: Urns.Api.Users)
class UsersApiV1(Api):
    def __init__(self, *args):
        super(UsersApiV1, self).__init__(args)

    @put('user')
    def put(self):
        login = self.request.params.get('login')
        email = self.request.params.get('email')
        password = self.request.body.decode()

        with create_transaction() as transaction:
            state = UserSql(login, password, email)
            transaction.add(state)
            return HTTPOk()

    @get('user/{user_id}')
    def get(self):
        print(1)
        user_id = self.request.matchdict.get('user_id')
        with create_transaction() as transaction:
            state = transaction.query(UserSql).filter(UserSql.id == user_id).first()
            return HTTPOk(state.val()) if state is not None \
                else HTTPNotFound(FailResult("UserNotFound", "Пользователь не найдена"))
