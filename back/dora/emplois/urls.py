from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r"orientations", views.OrientationViewSet, basename="orientation")

urlpatterns = [
    path(
        "orientations/status/",
        views.OrientationStatusListView.as_view(),
        name="orientation-status",
    ),
    path("", include(router.urls)),
    path(
        "mobilisation-event/",
        views.record_mobilisation_event,
        name="mobilisation-event",
    ),
]

app_name = "emplois"
