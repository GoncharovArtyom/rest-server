import requests
from random import randint
from http import HTTPStatus
from server.model import Message
from sqlalchemy.orm.session import Session


def test_post_message(server_messages_url, session, get_key):
    value = {"hello": "world"}
    key = get_key()

    response = requests.post(f"{server_messages_url}/{key}", json=value)
    message = session.query(Message).filter_by(key=key).first()

    assert response.status_code == HTTPStatus.CREATED
    assert message and message.value == value


def test_post_message_again(server_messages_url, get_key):
    value = {"hello": "world"}
    key = get_key()

    requests.post(f"{server_messages_url}/{key}", json=value)
    response = requests.post(f"{server_messages_url}/{key}", json=value)

    assert response.status_code == HTTPStatus.OK


def test_get_message(server_messages_url, get_key):
    value = {"hello": "world"}
    key = get_key()

    response = requests.post(f"{server_messages_url}/{key}", json=value)
    assert response.status_code == HTTPStatus.CREATED

    response = requests.get(f"{server_messages_url}/{key}")

    assert response.status_code == HTTPStatus.OK
    assert response.json() is not None and response.json() == value


def test_delete_message(server_messages_url, session, get_key):
    value = {"hello": "world"}
    key = get_key()

    response = requests.post(f"{server_messages_url}/{key}", json=value)
    assert response.status_code == HTTPStatus.CREATED

    response = requests.delete(f"{server_messages_url}/{key}")
    message = session.query(Message).filter_by(key=key).first()

    assert response.status_code == HTTPStatus.OK
    assert message is None
