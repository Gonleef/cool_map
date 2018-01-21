import logging
from core.response import HTTPBadResponse, HTTPForbidden, HTTPInternalServerError
from pyramid.request import Request
from pyramid.view import notfound_view_config, forbidden_view_config, exception_view_config


@notfound_view_config()
def not_found_view(req: Request):
    return HTTPBadResponse()


@forbidden_view_config()
def forbidden_view(req: Request):
    return HTTPForbidden()


@exception_view_config()
def exception_view(req: Request):
    logging.error("Fail to handle req: " + req.url, exc_info=True)
    return HTTPInternalServerError()


