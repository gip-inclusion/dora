from django.urls import path

from . import views

nexus_patterns = [
    path("nexus/auto-login-in/", views.auto_login_in, name="auto-login-in"),
]
