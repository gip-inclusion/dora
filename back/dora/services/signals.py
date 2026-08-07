"""Double écriture : maintient `Service.publics_di` / `publics_precisions` synchronisés avec la
relation M2M historique `publics` pendant leur coexistence (fenêtre de migration expand/contract).
"""

from django.db.models.signals import m2m_changed, post_delete, post_save, pre_delete
from django.dispatch import receiver

from dora.services.models import Public, Service
from dora.services.utils import compute_publics_di


def _sync(service):
    publics_di, publics_precisions = compute_publics_di(service)
    Service._base_manager.filter(pk=service.pk).update(
        publics_di=publics_di, publics_precisions=publics_precisions
    )
    # Garde l'instance en mémoire cohérente : un save() complet ultérieur de ce même objet
    # (p. ex. send_moderation_notification) réécrirait sinon des valeurs périmées.
    service.publics_di = publics_di
    service.publics_precisions = publics_precisions


def _sync_pks(pks):
    for service in Service._base_manager.filter(pk__in=pks):
        _sync(service)


@receiver(m2m_changed, sender=Service.publics.through)
def on_service_publics_changed(sender, instance, action, reverse, pk_set, **kwargs):
    # Reverse clear (`public.service_set.clear()`) : capturer les services avant que le clear
    # ne supprime les liens, pour les resynchroniser au post_clear.
    if reverse and action == "pre_clear":
        instance._cleared_service_pks = list(
            instance.service_set.values_list("pk", flat=True)
        )
        return

    if action not in ("post_add", "post_remove", "post_clear"):
        return

    if not reverse:
        # instance est un Service
        _sync(instance)
        return

    # instance est un Public
    if action == "post_clear":
        _sync_pks(getattr(instance, "_cleared_service_pks", []))
    else:
        _sync_pks(pk_set or [])


@receiver(post_save, sender=Public)
def on_public_saved(sender, instance, **kwargs):
    # les modifications de corresponding_di_publics / name changent les valeurs dérivées de chaque service lié.
    _sync_pks(instance.service_set.values_list("pk", flat=True))


@receiver(pre_delete, sender=Public)
def on_public_pre_delete(sender, instance, **kwargs):
    # Capturer les services liés avant que la suppression en cascade ne retire les liens M2M.
    instance._linked_service_pks = list(
        instance.service_set.values_list("pk", flat=True)
    )


@receiver(post_delete, sender=Public)
def on_public_deleted(sender, instance, **kwargs):
    # Les liens ont disparu : recalculer les services qui référençaient ce public.
    _sync_pks(getattr(instance, "_linked_service_pks", []))
