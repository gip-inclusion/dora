"""Double écriture : maintient `Service.publics_di` / `publics_precisions` synchronisés avec la
relation M2M historique `publics` pendant leur coexistence (fenêtre de migration expand/contract).
"""

from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from dora.services.models import Public, Service
from dora.services.utils import compute_publics_di


def _sync(service):
    publics_di, publics_precisions = compute_publics_di(service)
    Service.objects.filter(pk=service.pk).update(
        publics_di=publics_di, publics_precisions=publics_precisions
    )
    # Garde l'instance en mémoire cohérente : un save() complet ultérieur de ce même objet
    # (p. ex. send_moderation_notification) réécrirait sinon des valeurs périmées.
    service.publics_di = publics_di
    service.publics_precisions = publics_precisions


@receiver(m2m_changed, sender=Service.publics.through)
def on_service_publics_changed(sender, instance, action, reverse, pk_set, **kwargs):
    if action not in ("post_add", "post_remove", "post_clear"):
        return
    if not reverse:
        # instance est un Service
        _sync(instance)
    else:
        # instance est un Public ; recalcule chaque service concerné (tous les liés lors d'un clear)
        services = (
            Service.objects.filter(pk__in=pk_set)
            if pk_set
            else instance.service_set.all()
        )
        for service in services:
            _sync(service)


@receiver(post_save, sender=Public)
def on_public_saved(sender, instance, **kwargs):
    # les modifications de corresponding_di_publics / name changent les valeurs dérivées de chaque service lié.
    for service in instance.service_set.all():
        _sync(service)
