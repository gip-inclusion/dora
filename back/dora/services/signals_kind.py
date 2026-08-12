"""Double écriture : maintient `Service.kind` synchronisé avec la M2M historique `Service.kinds`
pendant leur coexistence.

Tant que le formulaire écrit `kinds`, `kind` en est dérivé après chaque modification, quel que
soit le chemin d'écriture (API, admin, imports, instanciation depuis un modèle, import CSV).
La commande `backfill_service_kind` sert de filet en cas de divergence.

Trois opérations demandent de relever les services liés *avant* que le signal « post » ne parte,
soit parce que les liens auront disparu (`kind.service_set.clear()`, suppression d'un
`ServiceKind`), soit pour savoir s'il y a lieu de recalculer (`pre_save`).

Un même type pouvant être lié à des dizaines de milliers de services, tout recalcul groupé passe
par `bulk_update` et on s'abstient dès que `value` n'a pas bougé.
"""

from django.db.models.signals import (
    m2m_changed,
    post_delete,
    post_save,
    pre_delete,
    pre_save,
)
from django.dispatch import receiver

from dora.services.models import Service, ServiceKind
from dora.services.utils import compute_service_kind

# attribut où sont mis de côté les services à recalculer entre le signal « pre » et le « post »
PENDING = "_dora_services_to_resync"
BATCH = 500


def _sync(service):
    kind = compute_service_kind(service)
    Service._base_manager.filter(pk=service.pk).update(kind=kind)
    # Garde l'instance en mémoire cohérente : un `save()` complet ultérieur de ce même objet
    # (p. ex. dans `instantiate_service_from_model`) réécrirait sinon une valeur périmée.
    service.kind = kind


def _sync_all(service_pks):
    """Recalcule en masse : un type peut être lié à des dizaines de milliers de services."""
    if not service_pks:
        return

    updated = []
    services = (
        Service._base_manager.filter(pk__in=service_pks)
        .only("pk")
        .prefetch_related("kinds")
        .iterator(chunk_size=BATCH)
    )
    for service in services:
        service.kind = compute_service_kind(service)
        updated.append(service)

        if len(updated) >= BATCH:
            Service._base_manager.bulk_update(updated, ["kind"])
            updated = []

    if updated:
        Service._base_manager.bulk_update(updated, ["kind"])


def _linked_service_pks(kind):
    return list(Service._base_manager.filter(kinds=kind).values_list("pk", flat=True))


@receiver(m2m_changed, sender=Service.kinds.through)
def on_service_kinds_changed(sender, instance, action, reverse, pk_set, **kwargs):
    if not reverse:
        # `instance` est un Service : ses liens suffisent à recalculer son type
        if action in ("post_add", "post_remove", "post_clear"):
            _sync(instance)
        return

    # `instance` est un ServiceKind
    if action == "pre_clear":
        setattr(instance, PENDING, _linked_service_pks(instance))
    elif action == "post_clear":
        _sync_all(getattr(instance, PENDING, None))
    elif action in ("post_add", "post_remove"):
        _sync_all(pk_set)


@receiver(pre_save, sender=ServiceKind)
def on_service_kind_saving(sender, instance, **kwargs):
    # Seul un changement de `value` modifie le type dérivé. Sans ce garde-fou, corriger un
    # libellé depuis l'admin recalculerait les dizaines de milliers de services liés.
    previous = (
        ServiceKind.objects.filter(pk=instance.pk)
        .values_list("value", flat=True)
        .first()
        if instance.pk
        else None
    )
    value_changed = previous is not None and previous != instance.value
    setattr(instance, PENDING, _linked_service_pks(instance) if value_changed else [])


@receiver(post_save, sender=ServiceKind)
def on_service_kind_saved(sender, instance, **kwargs):
    _sync_all(getattr(instance, PENDING, None))


@receiver(pre_delete, sender=ServiceKind)
def on_service_kind_deleting(sender, instance, **kwargs):
    # les lignes de la table de liaison partent en cascade sans émettre `m2m_changed`
    setattr(instance, PENDING, _linked_service_pks(instance))


@receiver(post_delete, sender=ServiceKind)
def on_service_kind_deleted(sender, instance, **kwargs):
    _sync_all(getattr(instance, PENDING, None))
