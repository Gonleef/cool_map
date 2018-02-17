from enum import Enum


class HTTPHeaders(Enum):
    CONTENT_TYPE = 'Content-Type'
    LOCATION = 'Location'
    AUTHORIZATION = 'Authorization'
    SET_COOKIE = 'Set-Cookie'
