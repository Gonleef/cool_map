from api.api import Api, default, autoroute
from api.entities_sql import UserSql, SessionStateSql, create_transaction
from core.entities import FailResultSimple
from core.http_method import HTTPMethod
from core.permissions import Permissions
from core.response import HTTPForbidden, HTTPOk, HTTPNotFound
from core.urns import Urns


@default(factory=lambda r: Urns.Api.Auth, permission=Permissions.Null)
class AuthApiV1(Api):
    def __init__(self, *args):
        super(AuthApiV1, self).__init__(args)

    @autoroute(HTTPMethod.POST)
    def authenticate_by_pass(self):
        login = self.request.params.get('login')
        client_addr = self.request.params.get('client_addr')
        password = self.request.body.decode()

        with create_transaction() as transaction:
            user = transaction.query(UserSql)\
                .filter((UserSql.login == login) & (UserSql.password == password))\
                .first()
            if user is None:
                return HTTPForbidden(FailResultSimple("UserNotFound", "Пользователь не найден"))

            state = SessionStateSql(user_id=user.id, auth_mode="ByPass", ip_address=client_addr)
            transaction.add(state)
            return HTTPOk(sid=state.id)

    @autoroute(HTTPMethod.GET, suffix='/{auth_sid}')
    def session(self):
        with create_transaction() as transaction:
            auth_sid = self.request.matchdict.get('auth_sid')
            state = transaction.query(SessionStateSql).filter(SessionStateSql.id == auth_sid).first()
            return HTTPOk(state.val()) if state is not None \
                else HTTPNotFound(FailResultSimple("SessionNotFound", "Сессия не найдена"))
