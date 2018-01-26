from clients.auth_client_v1 import AuthClient
from clients.auth_provider import IAuthProvider
from clients.form_client_v1 import FormClient
from clients.permissions_client_v1 import PermissionClient


class ApiClient(object):
    def __init__(self, auth: IAuthProvider):
        self.auth_client = AuthClient(auth)
        self.form_client = FormClient(auth)
        self.permission_client = PermissionClient(auth)
