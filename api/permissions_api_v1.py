from api.api import Api, default, route
from api.entities_sql import create_transaction, PermissionSql
from core.entities import Permission, ItemsResult
from core.http_method import HTTPMethod
from core.permissions import Permissions
from core.response import HTTPOk, HTTPNotFound
from core.urn import UserUrn, Urn
from core.urns import Urns


@default(factory=lambda r: Urns.Api.Permissions)
class PermissionApiV1(Api):
    def __init__(self, *args):
        super(PermissionApiV1, self).__init__(args)

    @route(HTTPMethod.GET, '/subject/{subject}/object/{object}')
    def get_permission(self):
        sub = Urn(self.request.matchdict.get('subject'))
        obj = Urn(self.request.matchdict.get('object'))
        return self._get_permission(sub, obj)

    @route(HTTPMethod.GET, '/object/{object}')
    def get_my_permission(self):
        sub = UserUrn(self.request.session.user_id)
        obj = Urn(self.request.matchdict.get('object'))
        return self._get_permission(sub, obj)

    @route(HTTPMethod.GET, '/subject/{subject}/list')
    def get_permissions(self):
        sub = Urn(self.request.matchdict.get('subject'))
        skip = int(self.request.params.get('skip', 0))
        take = int(self.request.params.get('take', 50000))
        return self._get_permissions(sub, skip, take)

    @route(HTTPMethod.GET, '/list')
    def get_my_permissions(self):
        sub = UserUrn(self.request.session.user_id)
        skip = int(self.request.params.get('skip', 0))
        take = int(self.request.params.get('take', 50000))
        return self._get_permissions(sub, skip, take)

    @staticmethod
    def _get_permission(sub: Urn, obj: Urn):
        with create_transaction() as transaction:
            permission = transaction.query(PermissionSql) \
                .filter((PermissionSql.subject == str(sub)) & (PermissionSql.object == str(obj)))\
                .first()
            return HTTPOk(permission.val()) if permission is not None \
                else HTTPNotFound(Permission(sub, obj, Permissions.Null))

    @staticmethod
    def _get_permissions(sub: Urn, skip: int, take: int):
        with create_transaction() as transaction:
            count = transaction.query(PermissionSql) \
                .filter(PermissionSql.subject == str(sub)) \
                .count()

            if count == 0 or skip >= count:
                return HTTPNotFound(ItemsResult([], skip, take, count))

            permissions = transaction.query(PermissionSql)\
                .filter(PermissionSql.subject == sub)\
                [skip:take]
            items = list(map(lambda p: p.val().__dict__, permissions))
            return HTTPOk(ItemsResult(items, skip, take, count))
