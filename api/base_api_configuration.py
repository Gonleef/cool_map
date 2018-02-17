import logging

from core.entities import FailResultSimple
from core.response import HTTPBadResponse, HTTPForbidden, HTTPInternalServerError
from pyramid.request import Request


def not_found_view(req: Request):
    return HTTPBadResponse()


def forbidden_view(req: Request):
    return HTTPForbidden(FailResultSimple('Forbidden', 'Authorization has been denied for this request'))


def exception_view(req: Request):
    logging.error("Fail to handle req: " + req.url, exc_info=True)
    return HTTPInternalServerError()


