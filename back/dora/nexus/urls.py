from django.urls import path

from . import views

nexus_patterns = [
    path("nexus/auto-login-in/", views.auto_login_in, name="auto-login-in"),
    path("nexus/auto-login-out/", views.auto_login_out, name="auto-login-out"),
    path("nexus/dropdown-status/", views.dropdown_status, name="dropdown-status"),
]
