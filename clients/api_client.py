from clients.auth_client_v1 import AuthClient
from clients.auth_provider import IAuthProvider
from clients.form_client_v1 import FormClient
from clients.permissions_client_v1 import PermissionClient
from clients.users_client_v1 import UsersClient


class ApiClient(object):
    def __init__(self, auth: IAuthProvider):
        self.auth_client = AuthClient()
        self.form_client = FormClient(auth)
        self.permission_client = PermissionClient(auth)
        self.users_client = UsersClient(auth)
