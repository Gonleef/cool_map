import sys
from clients.auth_provider import LoginAuthProvider


class Configuration(object):
    _settings: dict = dict()

    @classmethod
    def init(cls, package: str, **settings):
        package = package if package is not None else cls._get_package_name(2)
        cls._settings[package] = settings

    @classmethod
    def get(cls, package: str):
        package = package if package is not None else cls._get_package_name(2)
        return cls._settings.get(package)

    @classmethod
    def _get_package_name(cls, depth: int):
        package = sys._getframe(depth).f_globals.get('__name__', 'trash')
        if '.' in package:
            package = package[:package.index('.')]
        return package


class ConfigurationWrapper(Configuration):
    _auth_providers: dict = dict()

    @classmethod
    def get_auth(cls, package: str):
        package = package if package is not None else cls._get_package_name(2)
        settings = cls._settings.get(package)
        return cls._get_or_update(cls._auth_providers, package, lambda: LoginAuthProvider(settings.get('login'), settings.get('password')))

    @classmethod
    def _get_or_update(cls, cache: dict, key: str, provider):
        if key not in cache:
            cache[key] = provider()
        return cache[key]
