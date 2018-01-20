from pyramid.httpexceptions import *


def not_found_view(request):
    return HTTPNotFound()

