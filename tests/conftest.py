import itertools
import os
from typing import Callable

import pytest
import redis as rd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


@pytest.fixture
def server_messages_url() -> str:
    server_url = os.environ["SERVER_URL"]
    return server_url + "/messages"


@pytest.fixture
def balancer_messages_url() -> str:
    balancer_url = os.environ["BALANCER_URL"]
    return balancer_url + "/messages"


@pytest.fixture
def session() -> Session:
    database_url = os.environ["DATABASE_URL"]
    engine = create_engine(database_url)

    session_factory = sessionmaker(bind=engine)
    session = session_factory()

    try:
        yield session
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()


@pytest.fixture
def redis() -> rd.Redis:
    redis_host = os.environ["REDIS_HOST"]
    redis_port = os.environ["REDIS_PORT"]

    redis = rd.Redis(host=redis_host, port=redis_port)

    try:
        yield redis
    finally:
        redis.close()


@pytest.fixture(scope="session")
def get_key() -> Callable[[], int]:
    iterator = itertools.count()
    return iterator.__next__
