import uuid

from core.configuration import ConfigurationWrapper
from core.entities import *
from sqlalchemy import create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session

Base = declarative_base()
Engine = create_engine(ConfigurationWrapper.instance('api').get('database'))


class SessionWrapper(Session):
    def __init__(self, **kwargs):
        super(SessionWrapper, self).__init__(**kwargs)

    def __enter__(self) -> 'SessionWrapper':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        self.close()


def create_transaction() -> SessionWrapper:
    return SessionWrapper(bind=Engine)


class UserSql(Base):
    __table__ = Table('User', Base.metadata, autoload=True, autoload_with=Engine)
    id = __table__.c.Id
    login = __table__.c.Login
    password = __table__.c.Password
    email = __table__.c.Email

    def __init__(self, login: str, password: str, email: str = None, id: str = None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.login = login
        self.password = password
        self.email = email

    def val(self):
        return User(
            self.id,
            self.login,
            self.email)


class SessionStateSql(Base):
    __table__ = Table('SessionState', Base.metadata, autoload=True, autoload_with=Engine)
    id = __table__.c.Id
    user_id = __table__.c.UserId
    auth_mode = __table__.c.AuthMode
    creation_date = __table__.c.CreationDate
    ip_address = __table__.c.IPAddress

    def __init__(self, user_id: str, auth_mode: str = None, ip_address: str = None):
        self.id = uuid.uuid1().hex.upper() + uuid.uuid4().hex.upper()
        self.user_id = user_id
        self.auth_mode = auth_mode
        self.ip_address = ip_address

    def val(self):
        return SessionState(
            self.id,
            self.user_id,
            self.auth_mode,
            str(self.creation_date),
            self.ip_address)


class PermissionSql(Base):
    __table__ = Table('Permission', Base.metadata, autoload=True, autoload_with=Engine)
    subject = __table__.c.Subject
    object = __table__.c.Object
    value = __table__.c.Value

    def __init__(self, sub: str, obj: str, value: Permissions):
        self.subject = sub
        self.object = obj
        self.value = value.value

    def val(self):
        return Permission(
            Urn(self.subject),
            Urn(self.object),
            self.value)


class FormSql(Base):
    __table__ = Table('Form', Base.metadata, autoload=True, autoload_with=Engine)
    id = __table__.c.Id
    creator = __table__.c.Creator
    title = __table__.c.Title
    description = __table__.c.Description
    content = __table__.c.Content

    def __init__(self, creator: str, title: str, content: str, description: str = None, id: str = None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.creator = creator
        self.title = title
        self.content = content
        self.description = description

    def val(self):
        return Form(
            self.id,
            self.creator,
            self.title,
            self.description,
            self.content)


class AnswerSql(Base):
    __table__ = Table('Answer', Base.metadata, autoload=True, autoload_with=Engine)
    id = __table__.c.Id
    respondent_id = __table__.c.RespondentId
    form_id = __table__.c.FormId
    answer = __table__.c.Answer

    def __init__(self, respondent_id: str, form_id: str, answer: str, id: str = None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.respondent_id = respondent_id
        self.form_id = form_id
        self.answer = answer

    def val(self):
        return Answer(
            self.id,
            self.respondent_id,
            self.form_id,
            self.answer)


class BindingSql(Base):
    __table__ = Table('Binding', Base.metadata, autoload=True, autoload_with=Engine)
    form_id = __table__.c.FormId
    place_id = __table__.c.PlaceId

    def __init__(self, form_id: str, place_id: str):
        self.form_id = form_id
        self.place_id = place_id

    def val(self):
        return Binding(
            self.form_id,
            self.place_id)


class PlaceSql(Base):
    __table__ = Table('Place', Base.metadata, autoload=True, autoload_with=Engine)
    id = __table__.c.Id
    osm_type = __table__.c.Osm_type
    osm_id = __table__.c.Osm_id
    title = __table__.c.Title
    address = __table__.c.Address

    def __init__(self, osm_type: str, osm_id: int, title: str, address: str, id: str = None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.osm_type = osm_type
        self.osm_id = osm_id
        self.title = title
        self.address = address

    def val(self):
        return Place(
            self.id,
            self.osm_type,
            self.osm_id,
            self.title,
            self.address)
