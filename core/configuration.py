from clients.auth_provider import LoginAuthProvider


class Configuration(object):
    _settings: dict = dict()

    @classmethod
    def init(cls, **settings):
        package = cls._get_package_name()
        cls._settings[package] = settings

    @classmethod
    def get(cls):
        package = cls._get_package_name()
        return cls._settings.get(package)

    @classmethod
    def _get_package_name(cls):
        module = cls.__module__
        return module[:module.index('.')]


class ConfigurationWrapper(Configuration):
    _auth_providers: dict = dict()

    @classmethod
    def get_auth(cls):
        package = cls._get_package_name()
        settings = cls._settings.get(package)
        return cls._get_or_update(cls._auth_providers, package, lambda: LoginAuthProvider(settings.get('login'), settings.get('password')))

    @classmethod
    def _get_or_update(cls, cache: dict, key: str, provider):
        if key not in cache:
            cache[key] = provider()
        return cache[key]
