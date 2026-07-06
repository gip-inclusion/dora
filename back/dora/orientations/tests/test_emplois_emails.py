import re
import uuid
from datetime import datetime
from datetime import timezone as dt_timezone

import pytest
from django.conf import settings
from django.core import mail
from freezegun import freeze_time

from dora.core.test_utils import (
    make_emplois_orientation,
    make_service,
    make_structure,
)
from dora.orientations.emails import (
    send_message_to_beneficiary,
    send_message_to_prescriber,
    send_orientation_accepted_emails,
    send_orientation_created_emails,
    send_orientation_expiration_emails,
    send_orientation_rejected_emails,
    send_orientation_reminder_emails,
)


@pytest.fixture(autouse=True)
def _disable_debug_prefix(monkeypatch):
    # Module-level `debug` is captured at import; force False so subjects are
    # the non-debug branch regardless of ORIENTATION_EMAILS_DEBUG in the env.
    import dora.orientations.emails.dora as dora_mod
    import dora.orientations.emails.emplois as emplois_mod

    monkeypatch.setattr(dora_mod, "debug", False)
    monkeypatch.setattr(emplois_mod, "debug", False)


@pytest.fixture(autouse=True)
def _freeze_time():
    # Freeze creation_date and any timezone.now() reads so snapshots stay
    # stable across runs.
    with freeze_time("2025-01-15T10:00:00Z"):
        yield


@pytest.fixture
def orientation(db):
    structure = make_structure(
        name="Structure Portante",
        siret="12345678901234",
        address1="1 rue du Service",
        city="Testville",
        postal_code="75001",
    )
    service = make_service(
        id=uuid.UUID("00000000-0000-0000-0000-000000000042"),
        structure=structure,
        name="Le Service",
        contact_email="contact@example.com",
        contact_name="Contact Service",
        contact_phone="0100000004",
        address1="1 rue du Service",
        city="Testville",
        postal_code="75001",
    )
    return make_emplois_orientation(
        service=service,
        query_id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
        query_expires_at=datetime(2025, 2, 15, 10, 0, 0, tzinfo=dt_timezone.utc),
        beneficiary_first_name="Ben",
        beneficiary_last_name="Beneficiaire",
        beneficiary_email="beneficiaire@example.com",
        beneficiary_phone="0100000001",
        referent_first_name="Ref",
        referent_last_name="Referent",
        referent_email="referent@example.com",
        referent_phone="0100000002",
        emplois_data={
            "prescriber_email": "prescripteur@example.com",
            "prescriber_first_name": "Presc",
            "prescriber_last_name": "Ripteur",
            "prescriber_phone": "0100000003",
            "structure_name": "Structure Emplois",
            "structure_siret": "98765432101234",
        },
    )


def _from(name):
    return f'"{name}" <{settings.DEFAULT_FROM_EMAIL}>'


def _no_reply(name):
    return f'"{name}" <{settings.NO_REPLY_EMAIL}>'


def _env(subject):
    return f"[{settings.ENVIRONMENT.upper()}] {subject}"


def _find(to):
    for m in mail.outbox:
        if m.to == [to]:
            return m
    raise AssertionError(
        f"no mail addressed to {to}; got {[m.to for m in mail.outbox]}"
    )


def _assert(to, subject, from_email, reply_to):
    m = _find(to)
    assert m.subject == _env(subject), (m.subject, _env(subject))
    assert m.from_email == from_email, (m.from_email, from_email)
    assert m.reply_to == (reply_to or []), (m.reply_to, reply_to)
    return m


_UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def _bodies(outbox):
    # Redact UUIDs (service.id, orientation.query_id) so snapshots are stable
    # while keeping every other body content assertable.
    return {m.to[0]: _UUID_RE.sub("<UUID>", m.body) for m in outbox}


EMPLOIS_FROM = _no_reply("La plateforme de l'inclusion")
DEFAULT_DORA_FROM = _from("La plateforme DORA")


def test_created(orientation, snapshot):
    send_orientation_created_emails(orientation)

    prescriber_email = orientation.prescriber_info.email
    structure_email = orientation.get_contact_email()
    prescriber_full_name = orientation.prescriber_info.full_name

    assert len(mail.outbox) == 4
    _assert(
        structure_email,
        "Nouvelle demande d’orientation reçue",
        _from(f"{prescriber_full_name} via DORA"),
        [prescriber_email],
    )
    _assert(
        prescriber_email,
        "Votre demande a bien été transmise !",
        EMPLOIS_FROM,
        [structure_email],
    )
    _assert(
        orientation.referent_email,
        "Notification d’une demande d’orientation",
        EMPLOIS_FROM,
        [prescriber_email],
    )
    _assert(
        orientation.beneficiary_email,
        "Une orientation a été effectuée en votre nom",
        EMPLOIS_FROM,
        [prescriber_email],
    )
    assert _bodies(mail.outbox) == snapshot


def test_accepted(orientation, snapshot):
    send_orientation_accepted_emails(
        orientation,
        prescriber_message="adresse: #SERVICE_ADDRESS#",
        beneficiary_message="ben adresse: #SERVICE_ADDRESS#",
    )

    prescriber_email = orientation.prescriber_info.email
    structure_email = orientation.get_contact_email()
    service_address = orientation.get_service_address_line()

    assert len(mail.outbox) == 4
    _assert(
        structure_email,
        "Vous venez de valider une demande 🎉",
        DEFAULT_DORA_FROM,
        None,
    )
    p = _assert(
        prescriber_email,
        "Votre demande a été acceptée ! 🎉",
        EMPLOIS_FROM,
        [structure_email],
    )
    _assert(
        orientation.referent_email,
        "Notification de l’acceptation d’une demande d’orientation",
        EMPLOIS_FROM,
        [structure_email],
    )
    b = _assert(
        orientation.beneficiary_email,
        "Votre demande a été acceptée ! 🎉",
        EMPLOIS_FROM,
        [structure_email],
    )
    assert "#SERVICE_ADDRESS#" not in p.body
    assert service_address in p.body
    assert "#SERVICE_ADDRESS#" not in b.body
    assert service_address in b.body
    assert _bodies(mail.outbox) == snapshot


def test_rejected(orientation, snapshot):
    send_orientation_rejected_emails(orientation, message="nope")

    prescriber_email = orientation.prescriber_info.email
    structure_email = orientation.get_contact_email()

    assert len(mail.outbox) == 4
    _assert(
        structure_email,
        "Vous venez de refuser une demande",
        DEFAULT_DORA_FROM,
        None,
    )
    for to in (
        orientation.beneficiary_email,
        prescriber_email,
        orientation.referent_email,
    ):
        _assert(
            to,
            "Votre demande d’orientation a été refusée",
            EMPLOIS_FROM,
            [structure_email],
        )
    assert _bodies(mail.outbox) == snapshot


def test_expired(orientation, snapshot):
    from django.utils import timezone

    send_orientation_expiration_emails(orientation, start_date=timezone.now())

    prescriber_email = orientation.prescriber_info.email
    structure_email = orientation.get_contact_email()

    assert len(mail.outbox) == 4
    _assert(
        structure_email,
        "Cette demande d’orientation a expiré",
        DEFAULT_DORA_FROM,
        None,
    )
    _assert(
        prescriber_email,
        "Votre demande d’orientation a expiré",
        EMPLOIS_FROM,
        [structure_email],
    )
    _assert(
        orientation.referent_email,
        "Votre demande d’orientation a expiré",
        EMPLOIS_FROM,
        [structure_email],
    )
    _assert(
        orientation.beneficiary_email,
        "Cette demande d’orientation a été annulée",
        EMPLOIS_FROM,
        [structure_email],
    )
    assert _bodies(mail.outbox) == snapshot


def test_reminder(orientation, snapshot):
    send_orientation_reminder_emails(orientation)

    assert len(mail.outbox) == 1
    _assert(
        orientation.get_contact_email(),
        "Relance – Demande d’orientation en attente",
        DEFAULT_DORA_FROM,
        None,
    )
    assert _bodies(mail.outbox) == snapshot


def test_message_to_prescriber(orientation, snapshot):
    cc = ["someone@example.com"]
    send_message_to_prescriber(orientation, message="hello", cc=cc)

    structure_name = orientation.get_structure_name()

    assert len(mail.outbox) == 1
    m = _assert(
        orientation.prescriber_info.email,
        f"Vous avez un nouveau message de la structure {structure_name}",
        _from(f"{structure_name} via Les Emplois"),
        [orientation.get_contact_email()],
    )
    assert m.cc == cc
    assert _bodies(mail.outbox) == snapshot


def test_message_to_beneficiary(orientation, snapshot):
    cc = ["someone@example.com"]
    send_message_to_beneficiary(orientation, message="hello", cc=cc)

    structure_name = orientation.get_structure_name()

    assert len(mail.outbox) == 1
    m = _assert(
        orientation.beneficiary_email,
        f"Vous avez un nouveau message de la structure {structure_name}",
        _from(f"{structure_name} via Les Emplois"),
        [orientation.get_contact_email()],
    )
    assert m.cc == cc
    assert _bodies(mail.outbox) == snapshot
