from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(
    r"reference-data", views.ReferenceDataViewSet, basename="reference-data"
)
router.register(r"services", views.ServiceViewSet, basename="service")
router.register(
    r"disabled-dora-form-di-structures",
    views.DisabledDoraFormDIStructureViewSet,
    basename="disabled-dora-form-di-structure",
)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "emplois"
