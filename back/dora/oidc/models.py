from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.db import models


class UserSessionQueryset(models.QuerySet):
    def for_user(self, user):
        # retourne les informations de sessions pour un utilisateur donné
        return self.filter(user=user)


class UserSession(models.Model):
    """
    Permet d'identifier un utilisateur pour une session donnée et vice-versa.
    L'objet est détruit en cas de suppression de l'utilisateur ou de la session.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="utilisateur de la session",
        on_delete=models.CASCADE,
    )
    session = models.ForeignKey(
        Session,
        verbose_name="session Django",
        on_delete=models.CASCADE,
    )

    objects = UserSessionQueryset.as_manager()

    class Meta:
        verbose_name = "sessions pour un utilisateur"
        verbose_name_plural = "sessions pour un utilisateur"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "session"], name="unique_pair_user_session"
            )
        ]


def _session_created_handler(sender, request, user, **kwargs):
    UserSession.objects.get_or_create(user=user, session_id=request.session.session_key)


# On rattache la création ou la maj d'une session à un signal de connexion
user_logged_in.connect(_session_created_handler)
