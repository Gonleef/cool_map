from core.permissions import Permissions


class SessionState(object):
    def __init__(
            self,
            session_id: str,
            user_id: str,
            auth_mode: str,
            creation_date: str,
            ip_address: str):
        self.session_id = session_id
        self.user_id = user_id
        self.auth_mode = auth_mode
        self.creation_date = creation_date
        self.ip_address = ip_address


class FailResult(object):
    def __init__(
            self,
            status: str = 'UndefinedError',
            error_message: str = '',
            http_code: int = None,
            **kwargs):
        self.code = http_code
        self.status = status
        self.error_message = error_message
        self.__dict__.pop('code')


class ItemsResult(object):
    def __init__(
            self,
            items,
            skip: int,
            take: int,
            count: int):
        self.items = items
        self.skip = skip
        self.take = take
        self.count = count


class Permission(object):
    def __init__(
            self,
            subject: str,
            object: str,
            value: Permissions):
        self.subject = subject
        self.object = object
        self.value = value if isinstance(value, Permissions) \
            else Permissions(value)


class Form(object):
    def __init__(
            self,
            id: str,
            creator: str,
            title: str,
            description: str,
            content: str):
        self.id = id
        self.creator = creator
        self.title = title
        self.description = description
        self.content = content


class Answer(object):
    def __init__(self, respondent_id: str, form_id: str, answer: str):
        self.respondent_id = respondent_id
        self.form_id = form_id
        self.answer = answer


class User(object):
    def __init__(self, id: str, login: str, email: str):
        self.id = id
        self.login = login
        self.email = email
