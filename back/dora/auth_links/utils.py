import uuid

from django.core.cache import cache


def generate_auth_code(token_key: str):
    code = uuid.uuid4().hex
    cache.set(f"auth_code:{code}", token_key, timeout=60)
    return code
