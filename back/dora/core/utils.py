import logging
import re
from typing import Tuple

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.text import Truncator

logger = logging.getLogger(__name__)

TRUTHY_VALUES = ("1", 1, "True", "true", "t", "T", True)
FALSY_VALUES = ("0", 0, "False", "false", "f", "F", False)


def normalize_description(desc: str, limit: int) -> Tuple[str, str]:
    if len(desc) < limit:
        return desc, ""
    else:
        return Truncator(desc).chars(limit), desc


def normalize_phone_number(phone: str) -> str:
    if not phone:
        return phone
    has_intl_prefix = phone.strip().startswith("+")
    phone = "".join([c for c in phone if c.isdigit()])
    if has_intl_prefix:
        phone = re.sub("^330", "0", phone)
        phone = re.sub("^33", "0", phone)

    return phone[:10]


def code_insee_to_code_dept(code_insee):
    return code_insee[:3] if code_insee.startswith("97") else code_insee[:2]


def get_object_or_none(klass, *args, **kwargs):
    """
    Use get() to return an object, or return None if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    try:
        return get_object_or_404(klass, *args, **kwargs)
    except Http404:
        return None
