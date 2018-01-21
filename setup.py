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
    description='cool_map',
    keywords='web pyramid pylons',
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    packages=find_packages(),
    zip_safe=False,
    install_requires=requires,
    include_package_data=True,
    entry_points={
        'paste.app_factory': [
            'main_server = cool_map:get_app',
            'auth_server = auth:get_app',
        ],
    },
)
