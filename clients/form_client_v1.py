import json
import logging
from http import HTTPStatus

from clients.auth_provider import IAuthProvider
from core.entities import Answer, ItemsResult, FailResult, Form
from core.http_headers import HTTPHeaders
from core.operation_result import OperationResult
from pyramid.request import Request


class FormClient(object):
    def __init__(self, auth: IAuthProvider):
        self.auth = auth

    def get_answers(self, user_id: str, skip: int = 0, take: int = 50000):
        request = Request.blank('/api/form/v1/answers/for/%s?skip=%d&take=%d' % (user_id, skip, take))
        request.headers = {HTTPHeaders.AUTHORIZATION.value: self.auth.get_session_id()}
        response = request.get_response()
        data = json.loads(response.body.decode())
        if response.status_code != HTTPStatus.OK and response.status_code != HTTPStatus.NOT_FOUND:
            logging.warning('Fail to load answers for user ' + user_id + ': ' + data.get('error_message', ''))
            return OperationResult.fail(FailResult(http_code=response.status_code, **data))
        data['items'] = list(map(lambda o: Answer(**o), data.get('items', [])))
        return OperationResult.success(ItemsResult(**data))

    def get_form(self, form_id: str):
        request = Request.blank('/api/form/v1/form/' + form_id)
        request.headers = {HTTPHeaders.AUTHORIZATION.value: self.auth.get_session_id()}
        response = request.get_response()
        data = json.loads(response.body.decode())
        return OperationResult.success(Form(**data)) if response.status_code == HTTPStatus.OK \
            else OperationResult.fail(FailResult(http_code=response.status_code, **data))

    def get_forms(self, user_id: str, skip: int = 0, take: int = 50000):
        request = Request.blank('/api/form/v1/forms/for/%s?skip=%d&take=%d' % (user_id, skip, take))
        request.headers = {HTTPHeaders.AUTHORIZATION.value: self.auth.get_session_id()}
        response = request.get_response()
        data = json.loads(response.body.decode())
        if response.status_code != HTTPStatus.OK and response.status_code != HTTPStatus.NOT_FOUND:
            logging.warning('Fail to load forms for user ' + user_id + ': ' + data.get('error_message', ''))
            return OperationResult.fail(FailResult(http_code=response.status_code, **data))
        data['items'] = list(map(lambda o: Form(**o), data.get('items', [])))
        return OperationResult.success(ItemsResult(**data))
