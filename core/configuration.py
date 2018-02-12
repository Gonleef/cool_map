from clients.auth_provider import LoginAuthProvider, IAuthProvider


class Configuration(object):
    _auth: IAuthProvider

    Login: str = ''
    Password: str = ''

    @classmethod
    def init(cls, **settings):
        for key in settings:
            setattr(cls, key, settings.get(key))

    @classmethod
    def get_auth(cls):
        if not hasattr(cls, '_auth') or cls._auth is None:
            cls._auth = LoginAuthProvider(cls.Login, cls.Password)
        return cls._auth
