from core.api import Api
from core.response import HTTPForbidden, HTTPOk
from core.sql_entities import User, SessionState, create_transaction
from pyramid.request import Request
from pyramid.view import view_config


@view_config(match_param="version=v1")
class AuthApiV1(Api):
    def __init__(self, request: Request):
        super(AuthApiV1, self).__init__(request)

    @Api.post
    def authenticate_by_pass(self):
        with create_transaction() as transaction:
            login = self.request.params.get('login', '')
            password = self.request.body.decode()

            user = transaction.query(User)\
                .filter((User.login == login) & (User.password == password))\
                .first()
            if user is None:
                return HTTPForbidden(Code="UserNotFound", ErrorMessage="Пользователь не найден")

            state = SessionState(user_id=user.id, auth_mode="ByPass")
            transaction.add(state)
            return HTTPOk(Sid=state.id)

    @Api.post
    def authenticate_by_phone(self):
        return HTTPForbidden(Code="UserNotFound", ErrorMessage="Пользователь не найден")

    @Api.get
    def session(self):
        with create_transaction() as transaction:
            auth_sid = self.request.params.get('auth.sid', '')

            state = transaction.query(SessionState).filter(SessionState.id == auth_sid).first()
            if state is None:
                return HTTPForbidden(
                    Code="SessionNotFound",
                    ErrorMessage="Сессия не найдена")

            return HTTPOk(
                SessionId=state.id,
                UserId=state.user_id,
                AuthMode=state.auth_mode,
                CreationDate=state.creation_date.__str__(),
                IPAddress=state.ip_address)
