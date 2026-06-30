import pytest
from django.conf import settings
from django.core import mail
from model_bakery.random_gen import gen_email

from dora.core.test_utils import make_emplois_orientation
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


@pytest.fixture
def orientation(db):
    return make_emplois_orientation(
        beneficiary_email=gen_email(),
        referent_email=gen_email(),
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
    raise AssertionError(f"no mail addressed to {to}; got {[m.to for m in mail.outbox]}")


def _assert(to, subject, from_email, reply_to):
    m = _find(to)
    assert m.subject == _env(subject), (m.subject, _env(subject))
    assert m.from_email == from_email, (m.from_email, from_email)
    assert m.reply_to == (reply_to or []), (m.reply_to, reply_to)
    return m


EMPLOIS_FROM = _no_reply("La plateforme de l'inclusion")
DEFAULT_DORA_FROM = _from("La plateforme DORA")


def test_created(orientation):
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


def test_accepted(orientation):
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


def test_rejected(orientation):
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


def test_expired(orientation):
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


def test_reminder(orientation):
    send_orientation_reminder_emails(orientation)

    assert len(mail.outbox) == 1
    _assert(
        orientation.get_contact_email(),
        "Relance – Demande d’orientation en attente",
        DEFAULT_DORA_FROM,
        None,
    )


def test_message_to_prescriber(orientation):
    cc = ["someone@example.com"]
    send_message_to_prescriber(orientation, message="hello", cc=cc)

    structure_name = orientation.prescriber_info.structure_name

    assert len(mail.outbox) == 1
    m = _assert(
        orientation.prescriber_info.email,
        f"Vous avez un nouveau message de la structure {structure_name}",
        _from(f"{structure_name} via Les Emplois"),
        [orientation.get_contact_email()],
    )
    assert m.cc == cc


def test_message_to_beneficiary(orientation):
    cc = ["someone@example.com"]
    send_message_to_beneficiary(orientation, message="hello", cc=cc)

    structure_name = orientation.prescriber_info.structure_name

    assert len(mail.outbox) == 1
    m = _assert(
        orientation.beneficiary_email,
        f"Vous avez un nouveau message de la structure {structure_name}",
        _from(f"{structure_name} via Les Emplois"),
        [orientation.get_contact_email()],
    )
    assert m.cc == cc
