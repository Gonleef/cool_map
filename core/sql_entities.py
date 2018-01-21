import uuid

from sqlalchemy import create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import SessionTransaction, Session

Base = declarative_base()
Engine = create_engine('sqlite:///cool_map.db')


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


class User(Base):
    __table__ = Table('User', Base.metadata, autoload=True, autoload_with=Engine)
    id = __table__.c.Id
    login = __table__.c.Login
    password = __table__.c.Password
    email = __table__.c.Email

    def __init__(self, login: str, password: str, email: str = None):
        self.id = str(uuid.uuid4())
        self.login = login
        self.password = password
        self.email = email


class SessionState(Base):
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
