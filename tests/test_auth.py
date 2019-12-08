from http import HTTPStatus

import pytest
import requests
from requests.auth import HTTPBasicAuth

from balancer.auth.data import Role
from tests.utils import get_token_for


def test_create_token_existing_user(balancer_url):

    name = "reader"
    password = "123"

    response = requests.get(balancer_url + "/auth", auth=HTTPBasicAuth(name, password))

    assert "Authorization" in response.headers
    assert "Bearer " in response.headers["Authorization"]


def test_create_token_unknown_user(balancer_url):
    name = "reader1"
    password = "123"

    response = requests.get(balancer_url + "/auth", auth=HTTPBasicAuth(name, password))

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize("role", [Role.READER, Role.WRITER, Role.ADMIN])
def test_allowed_get(balancer_url, role: Role, get_key):

    token = get_token_for(balancer_url, role)

    key = get_key()
    response = requests.get(f"{balancer_url}/messages/{key}", headers={"Authorization": token})

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize("role", [Role.WRITER, Role.ADMIN])
def test_allowed_post(balancer_url, role: Role, get_key):

    token = get_token_for(balancer_url, role)

    value = {"hello": "world"}
    key = get_key()

    response = requests.post(f"{balancer_url}/messages/{key}", headers={"Authorization": token}, json=value)

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize("role", [Role.READER])
def test_restricted_post(balancer_url, role: Role, get_key):

    token = get_token_for(balancer_url, role)

    value = {"hello": "world"}
    key = get_key()

    response = requests.post(f"{balancer_url}/messages/{key}", headers={"Authorization": token}, json=value)

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_allowed_delete(balancer_url, get_key):
    token = get_token_for(balancer_url, Role.ADMIN)

    value = {"hello": "world"}
    key = get_key()

    response = requests.post(f"{balancer_url}/messages/{key}", headers={"Authorization": token}, json=value)
    assert response.status_code == HTTPStatus.CREATED

    response = requests.delete(f"{balancer_url}/messages/{key}", headers={"Authorization": token})
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize("role", [Role.READER, Role.WRITER])
def test_restricted_delete(balancer_url, role: Role, get_key):

    admin_token = get_token_for(balancer_url, Role.ADMIN)

    value = {"hello": "world"}
    key = get_key()

    response = requests.post(f"{balancer_url}/messages/{key}", headers={"Authorization": admin_token}, json=value)

    assert response.status_code == HTTPStatus.CREATED

    token = get_token_for(balancer_url, role)
    response = requests.delete(f"{balancer_url}/messages/{key}", headers={"Authorization": token})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


