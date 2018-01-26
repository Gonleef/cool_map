from setuptools import setup, find_packages

requires = [
    'pyramid',
    'pyramid_jinja2',
    'plaster_pastedeploy',
    'pyramid_debugtoolbar',
    'waitress',
    'sqlalchemy',
    'paste'
]


setup(
    name='cool_map',
    version='0.0',
    packages=find_packages(),
    install_requires=requires,
    include_package_data=True,
    entry_points={
        'paste.app_factory': [
            'api_server = api:get_app',
            'admin_server = admin:get_app',
            'main_server = map:get_app',
        ],
    },
)
