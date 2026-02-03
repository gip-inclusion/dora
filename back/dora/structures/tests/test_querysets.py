from dora.core.models import ModerationStatus
from dora.core.test_utils import make_service, make_structure, make_user
from dora.services.enums import ServiceStatus

from ..models import Structure, StructurePutativeMember


def test_orphan_structures():
    assert make_structure() in Structure.objects.orphans()
    assert make_structure(user=make_user()) not in Structure.objects.orphans()

    structure = make_structure()
    structure.members.add(make_user())

    assert structure not in Structure.objects.orphans()

    structure = make_structure()
    # il n'y a pas (encore?) de lien direct pour les membres invités, comme 'members'
    StructurePutativeMember(user=make_user(), structure=structure).save()

    assert structure not in Structure.objects.orphans()


def test_annotated_structures_for_admin():
    structure = make_structure()

    # Création de services avec différents statuts
    make_service(structure=structure, status=ServiceStatus.DRAFT)
    make_service(structure=structure, status=ServiceStatus.DRAFT)
    make_service(structure=structure, status=ServiceStatus.PUBLISHED)
    make_service(structure=structure, status=ServiceStatus.ARCHIVED)

    annotated = Structure.objects.annotated_structures_for_admin().get(id=structure.id)

    # Vérification de la présence des annotations
    assert hasattr(annotated, "num_draft_services")
    assert hasattr(annotated, "num_published_services")
    assert hasattr(annotated, "num_active_services")
    assert hasattr(annotated, "num_outdated_services")
    assert hasattr(annotated, "has_valid_admin")
    assert hasattr(annotated, "is_orphan")
    assert hasattr(annotated, "awaiting_moderation")
    assert hasattr(annotated, "is_waiting")
    assert hasattr(annotated, "categories_list")
    assert hasattr(annotated, "admin_emails")
    assert hasattr(annotated, "editor_emails")

    # Vérification des valeurs
    assert annotated.num_draft_services == 2
    assert annotated.num_published_services == 1
    assert annotated.num_active_services == 3  # DRAFT + PUBLISHED (pas ARCHIVED)
    assert annotated.is_orphan is True


def test_orphans_for_manager():
    manager_31 = make_user(is_manager=True, departments=["31"])
    manager_44 = make_user(is_manager=True, departments=["44"])

    # Structures orphelines dans différents départements
    orphan_31 = make_structure(department="31")
    orphan_31_2 = make_structure(department="31")
    orphan_44 = make_structure(department="44")
    orphan_75 = make_structure(department="75")

    # Structure non orpheline dans le département 31
    struct_with_member_31 = make_structure(department="31", user=make_user())

    # Vérification que le manager 31 voit seulement les structures orphelines du département 31
    orphans_manager_31 = Structure.objects.orphans_for_manager(manager_31)
    assert orphan_31 in orphans_manager_31
    assert orphan_31_2 in orphans_manager_31
    assert orphan_44 not in orphans_manager_31
    assert orphan_75 not in orphans_manager_31
    assert struct_with_member_31 not in orphans_manager_31

    # Vérification que le manager 44 voit seulement les structures orphelines du département 44
    orphans_manager_44 = Structure.objects.orphans_for_manager(manager_44)
    assert orphan_44 in orphans_manager_44
    assert orphan_31 not in orphans_manager_44
    assert orphan_31_2 not in orphans_manager_44
    assert orphan_75 not in orphans_manager_44
    assert struct_with_member_31 not in orphans_manager_44


def test_awaiting_moderation():
    # Structures en attente de modération
    awaiting_structure_1 = make_structure(
        is_obsolete=False,
        moderation_status=ModerationStatus.NEED_INITIAL_MODERATION,
    )
    awaiting_structure_1.members.add(
        make_user(is_valid=True, is_active=True),
        through_defaults={"is_admin": True},
    )
    awaiting_structure_2 = make_structure(
        is_obsolete=False,
        moderation_status=ModerationStatus.NEED_NEW_MODERATION,
    )
    awaiting_structure_2.members.add(
        make_user(is_valid=True, is_active=True),
        through_defaults={"is_admin": True},
    )

    # Structure validée (ne doit pas être dans le résultat)
    validated_structure = make_structure(
        is_obsolete=False,
        moderation_status=ModerationStatus.VALIDATED,
    )
    validated_structure.members.add(
        make_user(is_valid=True, is_active=True),
        through_defaults={"is_admin": True},
    )

    # Structure orpheline (ne doit pas être dans le résultat)
    orphan_structure = make_structure(
        is_obsolete=False,
        moderation_status=ModerationStatus.NEED_INITIAL_MODERATION,
    )

    # Structure obsolète (ne doit pas être dans le résultat)
    obsolete_structure = make_structure(
        is_obsolete=True,
        moderation_status=ModerationStatus.NEED_INITIAL_MODERATION,
    )
    obsolete_structure.members.add(
        make_user(is_valid=True, is_active=True),
        through_defaults={"is_admin": True},
    )

    # Test sans manager
    awaiting = Structure.objects.awaiting_moderation()
    assert awaiting_structure_1 in awaiting
    assert awaiting_structure_2 in awaiting
    assert validated_structure not in awaiting
    assert orphan_structure not in awaiting
    assert obsolete_structure not in awaiting

    # Test avec manager
    manager_31 = make_user(is_manager=True, departments=["31"])
    awaiting_structure_1.department = "31"
    awaiting_structure_1.save()

    awaiting_with_manager = Structure.objects.awaiting_moderation(manager_31)
    assert awaiting_structure_1 in awaiting_with_manager
    assert awaiting_structure_2 not in awaiting_with_manager
    assert validated_structure not in awaiting_with_manager
    assert orphan_structure not in awaiting_with_manager
    assert obsolete_structure not in awaiting_with_manager


def test_requiring_action_from_department_managers():
    # Structure orpheline
    orphan_structure = make_structure(department="31")

    # Structure en attente de modération
    awaiting_structure = make_structure(
        department="31",
        is_obsolete=False,
        moderation_status=ModerationStatus.NEED_INITIAL_MODERATION,
    )
    awaiting_structure.members.add(
        make_user(is_valid=True, is_active=True),
        through_defaults={"is_admin": True},
    )

    # Structure validée avec membre (ne doit pas être dans le résultat)
    validated_structure = make_structure(
        department="31",
        is_obsolete=False,
        moderation_status=ModerationStatus.VALIDATED,
    )
    validated_structure.members.add(
        make_user(is_valid=True, is_active=True),
        through_defaults={"is_admin": True},
    )

    requiring_action = Structure.objects.requiring_action_from_department_managers()

    # Vérification que les structures orphelines sont incluses
    assert orphan_structure in requiring_action

    # Vérification que les structures en attente de modération sont incluses
    assert awaiting_structure in requiring_action

    # Vérification que les structures validées ne sont pas incluses
    assert validated_structure not in requiring_action
