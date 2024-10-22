import random

from django.utils import timezone
from django.utils.crypto import get_random_string
from model_bakery import baker

from dora.services.enums import ServiceStatus
from dora.services.models import ServiceCategory, ServiceSubCategory
from dora.services.utils import update_sync_checksum


def make_user(structure=None, is_valid=True, is_admin=False, **kwargs):
    user = baker.make("users.User", is_valid=is_valid, **kwargs)
    if structure:
        structure.members.add(
            user,
            through_defaults={
                "is_admin": is_admin,
            },
        )

    return user


def make_structure(user=None, putative_member=None, **kwargs):
    siret = kwargs.pop("siret", None)
    if not siret:
        siret = get_random_string(14, "0123456789")
    latitude = kwargs.pop("latitude", None)
    if not latitude:
        latitude = random.random() * 90.0

    longitude = kwargs.pop("longitude", None)
    if not longitude:
        longitude = random.random() * 90.0
    structure = baker.make(
        "Structure",
        siret=siret,
        longitude=longitude,
        latitude=latitude,
        modification_date=timezone.now(),
        **kwargs,
    )
    if user:
        structure.members.add(user)

    if putative_member:
        structure.putative_membership.add(
            baker.make(
                "StructurePutativeMember", user=putative_member, structure=structure
            )
        )

    return structure


def make_service(**kwargs):
    structure = (
        kwargs.pop("structure")
        if "structure" in kwargs
        else make_structure(user=make_user())
    )
    categories = kwargs.pop("categories").split(",") if "categories" in kwargs else []
    subcategories = (
        kwargs.pop("subcategories").split(",") if "subcategories" in kwargs else []
    )
    modification_date = (
        kwargs.pop("modification_date") if "modification_date" in kwargs else None
    )

    service = baker.make(
        "Service",
        structure=structure,
        is_model=False,
        modification_date=modification_date if modification_date else timezone.now(),
        **kwargs,
    )
    if categories:
        db_cats = ServiceCategory.objects.filter(value__in=categories)
        assert db_cats.count() == len(categories)
        service.categories.set(db_cats)
    if subcategories:
        db_subcats = ServiceSubCategory.objects.filter(value__in=subcategories)
        assert db_subcats.count() == len(subcategories)
        service.subcategories.set(db_subcats)

    return service


def make_published_service(**kwargs):
    return make_service(status=ServiceStatus.PUBLISHED, **kwargs)


def make_model(**kwargs):
    structure = kwargs.pop("structure") if "structure" in kwargs else make_structure()
    model = baker.make(
        "ServiceModel",
        structure=structure,
        is_model=True,
        modification_date=timezone.now(),
        **kwargs,
    )
    model.sync_checksum = update_sync_checksum(model)
    model.save()
    return model


def make_orientation(**kwargs):
    prescriber_structure = make_structure()
    prescriber = (
        kwargs.pop("prescriber")
        if "prescriber" in kwargs
        else make_user(structure=prescriber_structure)
    )
    service = (
        kwargs.pop("service")
        if "service" in kwargs
        else make_service(
            _fill_optional=["contact_email"],
        )
    )
    orientation = baker.make(
        "Orientation",
        prescriber=prescriber,
        service=service,
        **kwargs,
    )
    return orientation
