from enum import Enum


class Role(Enum):
    READER = "reader"
    WRITER = "writer"
    ADMIN = "admin"


NAMES_TO_PASSWORDS = {
    "reader": "123",
    "writer": "123",
    "admin": "123",
}

NAMES_TO_ROLES = {role.value: role for role in Role}

SECRET_KEY = "SECRET_KEY"
