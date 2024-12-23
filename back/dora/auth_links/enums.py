import enum


class AuthLinkAction(enum.StrEnum):
    """
    Actions loggées pour les liens d'identifications.
    """

    SENT_AUTH_LINK = "sent_auth_link"
    DID_AUTHENTICATE_WITH_AUTH_LINK = "did_authenticate_with_auth_link"
    USED_EXPIRED_AUTH_LINK = "used_expired_auth_link"
