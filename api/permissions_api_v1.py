from api.api import Api, get, default
from core.entities import Permission
from core.entities_sql import create_transaction, PermissionSql
from core.permissions import Permissions
from core.response import HTTPOk, HTTPNotFound
from core.urns import Urns


@default(factory=lambda r: Urns.Api.Permissions)
class PermissionApiV1(Api):
    def __init__(self, *args):
        super(PermissionApiV1, self).__init__(args)

    @get('/user/{user_id}/object/{object}', permission=Permissions.Auth)
    def get_user_permission(self):
        sub = 'user:' + self.request.matchdict.get('user_id')
        obj = self.request.matchdict.get('object')
        return self._get_permission(sub, obj)

    @get('/object/{object}', permission=Permissions.Auth)
    def get_my_permission(self):
        sub = 'user:' + self.request.session.user_id
        obj = self.request.matchdict.get('object')
        return self._get_permission(sub, obj)

    @staticmethod
    def _get_permission(sub: str, obj: str):
        with create_transaction() as transaction:
            permission = transaction.query(PermissionSql) \
                .filter((PermissionSql.subject == sub) & (PermissionSql.object == obj))\
                .first()
            return HTTPOk(permission.val()) if permission is not None \
                else HTTPNotFound(Permission(sub, obj, Permissions.Null))
