from django.urls import path

import dora.oidc.views as views

oidc_patterns = [
    path(
        "inclusion-connect-get-login-info/",
        views.inclusion_connect_get_login_info,
    ),
    path(
        "inclusion-connect-get-logout-info/",
        views.inclusion_connect_get_logout_info,
    ),
    path(
        "inclusion-connect-get-update-info/",
        views.inclusion_connect_get_update_info,
    ),
    path(
        "inclusion-connect-authenticate/",
        views.inclusion_connect_authenticate,
    ),
]
