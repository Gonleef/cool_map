from enum import Enum

from core.urn import Urn


class Urns(object):

    class Api(Enum):
        __nid = 'api'
        Auth = Urn(__nid, 'auth')
        Users = Urn(__nid, 'users')
        Forms = Urn(__nid, 'forms')
        Permissions = Urn(__nid, 'permissions')

    class Admin(object):
        __nid = 'admin'
        Index = Urn(__nid, 'index')
        Enter = Urn(__nid, 'enter')
        Answers = Urn(__nid, 'answers')
        Form = Urn(__nid, 'form')
        Forms = Urn(__nid, 'forms')
        User = Urn(__nid, 'user')
