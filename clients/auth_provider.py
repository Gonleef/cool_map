from abc import ABCMeta, abstractmethod

from clients.auth_client_v1 import AuthClient


class IAuthProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_session_id(self):
        pass


class SessionAuthProvider(IAuthProvider):
    def __init__(self, session):
        self.session = session

    def get_session_id(self):
        return self.session


class FakeAuthProvider(SessionAuthProvider):
    def __init__(self):
        super(FakeAuthProvider, self).__init__('FAKE_SESSION_ID')


class LoginAuthProvider(IAuthProvider):
    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.session = None

    def get_session_id(self):
        if self.session is None:
            result = AuthClient().authenticate_by_pass(self.login, self.password)
            if result.is_success:
                self.session = result.data
        return self.session
