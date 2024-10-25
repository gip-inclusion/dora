from django.urls import path

from . import views

auth_links_patterns = [
    path("auth/send-link/", views.send_link, name="send_link"),
    path(
        "auth/authenticate-with-link/",
        views.authenticate_with_link,
        name="authenticate_with_link",
    ),
]
