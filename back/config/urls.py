from django.conf import settings
from django.contrib import admin
from django.urls import include, path, register_converter
from rest_framework.routers import SimpleRouter

import dora.core.views
import dora.decoupage_administratif.views
import dora.orientations.views
import dora.services.views
import dora.sirene.views
import dora.stats.views
import dora.structures.views
import dora.support.views
import dora.users.views
from dora.auth_links.urls import auth_links_patterns
from dora.nexus.urls import nexus_patterns
from dora.oidc.urls import oidc_patterns

from .url_converters import InseeCodeConverter, SiretConverter

router = SimpleRouter()
router.register(
    r"structures", dora.structures.views.StructureViewSet, basename="structure"
)
router.register(
    r"structure-members",
    dora.structures.views.StructureMemberViewset,
    basename="structure-member",
)
router.register(
    r"structure-putative-members",
    dora.structures.views.StructurePutativeMemberViewset,
    basename="structure-putative-member",
)
router.register(r"services", dora.services.views.ServiceViewSet, basename="service")
router.register(r"bookmarks", dora.services.views.BookmarkViewSet, basename="bookmark")
router.register(r"models", dora.services.views.ModelViewSet, basename="model")
router.register(
    r"saved-searches", dora.services.views.SavedSearchViewSet, basename="saved-search"
)

router.register(
    r"structures-admin",
    dora.support.views.StructureAdminViewSet,
    basename="structure-admin",
)

router.register(
    r"services-admin",
    dora.support.views.ServiceAdminViewSet,
    basename="service-admin",
)
router.register(
    r"orientations",
    dora.orientations.views.OrientationViewSet,
    basename="orientation",
)

register_converter(InseeCodeConverter, "insee_code")
register_converter(SiretConverter, "siret")


private_api_patterns = [
    path("auth/", include("dora.rest_auth.urls")),
    path(
        "search/",
        dora.services.views.search,
    ),
    path("stats/event/", dora.stats.views.log_event),
    path("services-di/<str:di_id>/", dora.services.views.service_di),
    path(
        "services-di/<str:di_id>/share/",
        dora.services.views.share_di_service,
    ),
    path(
        "services-di/<str:di_id>/feedback/",
        dora.services.views.post_di_service_feedback,
    ),
    path("admin-division-search/", dora.decoupage_administratif.views.search),
    path(
        "admin-division-reverse-search/",
        dora.decoupage_administratif.views.reverse_search,
    ),
    path(
        "admin-division-departments/",
        dora.decoupage_administratif.views.get_departments,
    ),
    path(
        "city-label/<insee_code:insee_code>/",
        dora.decoupage_administratif.views.get_city_label,
    ),
    path("search-sirene/<insee_code:citycode>/", dora.sirene.views.search_sirene),
    path("search-siret/", dora.sirene.views.search_siret),
    path("search-safir/", dora.sirene.views.search_safir),
    path("services-options/", dora.services.views.options),
    path("siret-claimed/<siret:siret>/", dora.structures.views.siret_was_claimed),
    path("structures-options/", dora.structures.views.options),
    path("upload/<slug:structure_slug>/<str:filename>/", dora.core.views.upload),
    path("safe-upload/<str:filename>/", dora.core.views.safe_upload),
    path("admin/", admin.site.urls),
    path("ping/", dora.core.views.ping),
    path("sentry-debug/", dora.core.views.trigger_error),
    path("", include(router.urls)),
    path("profile/", dora.users.views.update_user_profile),
    path(
        "profile/main-activity/", dora.users.views.update_user_profile
    ),  # TODO: remove when not used by frontend anymore
    path("consent-record/", dora.users.views.record_consent),
    path(
        "structures/<slug:structure_slug>/orientations/stats/",
        dora.orientations.views.display_orientation_stats,
    ),
    path(
        "structures/<slug:structure_slug>/orientations/export/",
        dora.orientations.views.OrientationExportView.as_view(),
    ),
]

di_api_patterns = [
    path("api/v2/", include("dora.api.urls", namespace="v2")),
]


urlpatterns = [
    *private_api_patterns,
    *di_api_patterns,
    # anciennes routes Inclusion-Connect (en attente de suppression)
    *oidc_patterns,
    # nouvelles routes OIDC pour ProConnect
    path("oidc/", include("mozilla_django_oidc.urls")),
    # "magic links"
    *auth_links_patterns,
    *nexus_patterns,
]

if settings.PROFILE:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
