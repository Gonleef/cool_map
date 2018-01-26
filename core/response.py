from http import HTTPStatus
from core.http_headers import HTTPHeaders
from pyramid.response import Response
import json


class HTTPResponse(Response):
    def __init__(self, obj=None, **kwargs):
        Response.__init__(self)
        self.headers[HTTPHeaders.CONTENT_TYPE.value] = 'application/json; charset=utf-8'
        result = obj.__dict__.copy() if obj is not None else dict()
        result.update(kwargs)
        self.body = json.dumps(result).encode()


class HTTPForbidden(HTTPResponse):
    def __init__(self, obj=None, **kwargs):
        HTTPResponse.__init__(self, obj, **kwargs)
        self.status = HTTPStatus.FORBIDDEN


class HTTPBadResponse(HTTPResponse):
    def __init__(self, obj=None, **kwargs):
        HTTPResponse.__init__(self, obj, **kwargs)
        self.status = HTTPStatus.BAD_REQUEST


class HTTPOk(HTTPResponse):
    def __init__(self, obj=None, **kwargs):
        HTTPResponse.__init__(self, obj, **kwargs)
        self.status = HTTPStatus.OK


class HTTPTemporaryRedirect(HTTPResponse):
    def __init__(self, ref: str):
        HTTPResponse.__init__(self)
        self.status = HTTPStatus.TEMPORARY_REDIRECT
        self.headers[HTTPHeaders.LOCATION.value] = ref


class HTTPInternalServerError(HTTPResponse):
    def __init__(self, obj=None, **kwargs):
        HTTPResponse.__init__(self, obj, **kwargs)
        self.status = HTTPStatus.INTERNAL_SERVER_ERROR


class HTTPNotFound(HTTPResponse):
    def __init__(self, obj=None, **kwargs):
        HTTPResponse.__init__(self, obj, **kwargs)
        self.status = HTTPStatus.NOT_FOUND
