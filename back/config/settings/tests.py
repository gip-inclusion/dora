import os
from unittest import mock

import pytest

from .utils import env_list, env_set


@pytest.mark.parametrize(
    ("env_value", "expected"),
    [
        (None, []),
        ("", []),
        ("   ", []),
        (",", []),
        ("value-1", ["value-1"]),
        ("value-1,value-2", ["value-1", "value-2"]),
        (" value-1 , value-2 ", ["value-1", "value-2"]),
        ("value-1,,value-2,", ["value-1", "value-2"]),
    ],
)
def test_env_list(env_value, expected):
    with mock.patch.dict(os.environ):
        os.environ.pop("A_VARIABLE", None)
        if env_value is not None:
            os.environ["A_VARIABLE"] = env_value

        assert env_list("A_VARIABLE") == expected


def test_env_list_default_value():
    with mock.patch.dict(os.environ):
        os.environ.pop("A_VARIABLE", None)

        assert env_list("A_VARIABLE", default="value-1,value-2") == [
            "value-1",
            "value-2",
        ]


def test_env_list_default_value_is_ignored_when_variable_is_set():
    with mock.patch.dict(os.environ, {"A_VARIABLE": "value-3"}):
        assert env_list("A_VARIABLE", default="value-1") == ["value-3"]


def test_env_list_preserves_order():
    with mock.patch.dict(os.environ, {"A_VARIABLE": "value-2,value-1"}):
        assert env_list("A_VARIABLE") == ["value-2", "value-1"]


@pytest.mark.parametrize(
    ("env_value", "expected"),
    [
        (None, frozenset()),
        ("", frozenset()),
        ("   ", frozenset()),
        (",", frozenset()),
        ("value-1", frozenset({"value-1"})),
        ("value-1,value-2", frozenset({"value-1", "value-2"})),
        (" value-1 , value-2 ", frozenset({"value-1", "value-2"})),
        ("value-1,,value-2,", frozenset({"value-1", "value-2"})),
        # les doublons sont dédoublonnés
        ("value-1,value-1", frozenset({"value-1"})),
    ],
)
def test_env_set(env_value, expected):
    with mock.patch.dict(os.environ):
        os.environ.pop("A_VARIABLE", None)
        if env_value is not None:
            os.environ["A_VARIABLE"] = env_value

        assert env_set("A_VARIABLE") == expected


def test_env_set_is_immutable():
    with mock.patch.dict(os.environ, {"A_VARIABLE": "value-1"}):
        assert isinstance(env_set("A_VARIABLE"), frozenset)
