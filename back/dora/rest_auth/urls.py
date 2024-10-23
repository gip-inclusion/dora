from django.urls import path

from . import views

urlpatterns = [
    path("user-info/", views.user_info, name="user-info"),
    path("join-structure/", views.join_structure, name="join-structure"),
    path("invite-first-admin/", views.invite_first_admin, name="invite-first-admin"),
    path("accept-cgu/", views.accept_cgu, name="accept-cgu"),
]
