from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r"structures", views.StructureViewSet, basename="structure")
router.register(r"services", views.ServiceViewSet, basename="service")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "api"
