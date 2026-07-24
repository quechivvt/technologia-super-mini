from enum import Enum


class UserEvent(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    REGISTER = "register"


class ProductEvent(str, Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"