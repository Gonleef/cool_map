from abc import ABCMeta, abstractmethod


class IAuthProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_session_id(self):
        pass


class SessionAuthProvider(IAuthProvider):
    def __init__(self, session):
        self.session = session

    def get_session_id(self):
        return self.session
