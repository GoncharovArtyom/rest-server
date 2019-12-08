import requests
from requests.auth import HTTPBasicAuth

from balancer.auth.data import Role


def get_token_for(balancer_url, role: Role) -> str:

    response = requests.get(balancer_url + "/auth", auth=HTTPBasicAuth(role.value, "123"))

    assert "Authorization" in response.headers
    assert "Bearer " in response.headers["Authorization"]

    return response.headers["Authorization"]
