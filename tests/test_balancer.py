import json
from http import HTTPStatus
from random import randint
from server.model import Message

import requests


def test_handle_post(balancer_messages_url, session, get_key):
    value = {"hello": "world"}
    key = get_key()
    print(key)

    response = requests.post(f"{balancer_messages_url}/{key}", json=value)
    message = session.query(Message).filter_by(key=key).first()

    assert response.status_code == HTTPStatus.CREATED
    assert message is not None


def test_handle_delete(balancer_messages_url, session, get_key):
    value = {"hello": "world"}
    key = get_key()
    print(key)

    response = requests.post(f"{balancer_messages_url}/{key}", json=value)
    assert response.status_code == HTTPStatus.CREATED
    response = requests.delete(f"{balancer_messages_url}/{key}")
    message = session.query(Message).filter_by(key=key).first()

    assert response.status_code == HTTPStatus.OK
    assert message is None


def test_store_in_cache_on_get(balancer_messages_url, server_messages_url, redis, get_key):
    value = {"hello": "world"}
    key = get_key()
    print(key)

    response = requests.post(f"{server_messages_url}/{key}", json=value)
    assert response.status_code == HTTPStatus.CREATED
    assert redis.get(key) is None

    response = requests.get(f"{balancer_messages_url}/{key}")
    assert response.status_code == HTTPStatus.OK
    assert redis.get(key) is not None and json.loads(redis[key].decode()) == value


def test_clear_cache_on_post(balancer_messages_url, server_messages_url, redis, get_key):
    value = {"hello": "world"}
    key = get_key()
    print(key)

    response = requests.post(f"{server_messages_url}/{key}", json=value)
    assert response.status_code == HTTPStatus.CREATED
    response = requests.get(f"{balancer_messages_url}/{key}")
    assert response.status_code == HTTPStatus.OK

    response = requests.post(f"{balancer_messages_url}/{key}", json=value)

    assert response.status_code == HTTPStatus.OK
    assert redis.get(key) is None


def test_clear_cache_on_delete(balancer_messages_url, server_messages_url, redis, get_key):
    value = {"hello": "world"}
    key = get_key()
    print(key)

    response = requests.post(f"{server_messages_url}/{key}", json=value)
    assert response.status_code == HTTPStatus.CREATED
    response = requests.get(f"{balancer_messages_url}/{key}")
    assert response.status_code == HTTPStatus.OK

    response = requests.delete(f"{balancer_messages_url}/{key}", json=value)

    assert response.status_code == HTTPStatus.OK
    assert redis.get(key) is None
