class Configuration(object):
    @classmethod
    def init(cls, **settings):
        setattr(cls, 'Login', settings.get('login'))
        setattr(cls, 'Password', settings.get('password'))
        setattr(cls, 'Sid', settings.get('sid'))
