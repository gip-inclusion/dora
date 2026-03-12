import os
import time

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from itoutils.django.nexus.token import generate_token

SERVICE_URL = "http://localhost:3000/services/tih-booster-haute-ga-tih-booster-31-linkl"


def gen_autologin_jwt() -> str:
    return generate_token(
        {"email": "gerald.gounot@inclusion.gouv.fr", "exp": int(time.time()) + 86400}
    )


def gen_op_jwt() -> str:
    return generate_token(
        {
            "beneficiary": {
                "email": "demo.emplois+19@inclusion.gouv.fr",
                "first_name": "Boris",
                "france_travail_id": "12345678909",
                "last_name": "Baracus",
                "phone": "0603897899",
                "uid": "2090b92d-9d6c-47ea-a7cd-97f8732c2298",
            },
            "prescriber": {
                "email": "gerald.gounot@inclusion.gouv.fr",
                "organization": {
                    "siret": "13003013300016",
                    "uid": "7a563d1d-4bcf-47b7-9493-639be48f2674",
                },
            },
            "exp": int(time.time()) + 86400,
        }
    )


autologin_jwt = gen_autologin_jwt()
op_jwt = gen_op_jwt()

print(f"{SERVICE_URL}?auto_login={autologin_jwt}&op={op_jwt}")
