from django.db.models import Q
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from dora.core.utils import (
    code_insee_to_code_dept,
    get_category_from_subcategory,
    get_object_or_none,
)
from dora.orientations.models import Orientation
from dora.services.models import (
    LocationKind,
    Service,
    ServiceCategory,
    ServiceFee,
    ServiceKind,
    ServiceSubCategory,
)
from dora.stats.models import (
    DiMobilisationEvent,
    DiServiceView,
    MobilisationEvent,
    OrientationView,
    SearchView,
    ServiceShare,
    ServiceView,
    StructureInfosView,
    StructureView,
)
from dora.structures.models import Structure, StructureMember

from .enums import Tag
from .models import PageView


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def log_event(request):
    def get_categories(cats_values, subcats_values):
        # On loggue également toutes les catégories des sous-catégories demandées
        subcats_cats_values = set(
            get_category_from_subcategory(subcat) for subcat in subcats_values
        )

        all_categories = ServiceCategory.objects.filter(
            Q(value__in=cats_values) | Q(value__in=subcats_cats_values)
        )

        all_subcategories = ServiceSubCategory.objects.filter(value__in=subcats_values)
        for category_value in cats_values:
            all_subcategories |= ServiceSubCategory.objects.filter(
                value__startswith=category_value
            )
        return all_categories, all_subcategories

    tag = request.data.get("tag")
    service_slug = request.data.get("service", "")
    structure_slug = request.data.get("structure", "")
    service = structure = orientation = None
    orientation_id = request.data.get("orientation", "")

    search_view = None
    search_view_id = request.data.get("search_id")
    if search_view_id:
        try:
            search_view = SearchView.objects.get(id=search_view_id)
        except (SearchView.DoesNotExist, ValueError):
            search_view = None

    if orientation_id:
        orientation = get_object_or_none(Orientation, id=orientation_id)
        if orientation:
            service = orientation.service
            structure = orientation.service.structure if service else None
    if not service and service_slug:
        service = get_object_or_none(Service, slug=service_slug)
        if service:
            structure = service.structure
    if not structure and structure_slug:
        structure = get_object_or_none(Structure, slug=structure_slug)

    user = request.user

    common_analytics_data = {
        "path": request.data.get("path"),
        "user": user if user.is_authenticated else None,
        "is_logged": user.is_authenticated,
        "is_staff": user.is_staff,
        "is_manager": user.is_manager if user.is_authenticated else False,
        "is_an_admin": StructureMember.objects.filter(user=user, is_admin=True).exists()
        if user.is_authenticated
        else False,
        "user_kind": user.main_activity if user.is_authenticated else "",
        "anonymous_user_hash": request.data.get("user_hash", ""),
    }

    structure_membership = (
        StructureMember.objects.filter(structure_id=structure.id, user=user).first()
        if structure and user.is_authenticated
        else None
    )
    structure_data = {
        "structure": structure,
        "is_structure_member": structure_membership is not None,
        "is_structure_admin": structure_membership.is_admin
        if structure_membership
        else False,
        "structure_department": structure.department if structure else "",
        "structure_city_code": structure.city_code if structure else "",
        "structure_source": structure.source.value
        if structure and structure.source
        else "",
    }

    service_data = {
        "service": service,
        "update_needed": service.get_update_needed() if service else "",
        "status": service.status if service else "",
        "service_source": service.source.value if service and service.source else "",
        "search_view": search_view,
    }

    di_service_data = {
        "structure_id": request.data.get("di_structure_id", ""),
        "structure_name": request.data.get("di_structure_name", ""),
        "structure_department": request.data.get("di_structure_department", ""),
        "service_id": request.data.get("di_service_id", ""),
        "service_name": request.data.get("di_service_name", ""),
        "source": request.data.get("di_source", ""),
        "search_view": search_view,
        "search_view_id": search_view_id,
    }

    event = None

    match tag:
        case Tag.PAGEVIEW:
            event = PageView.objects.create(
                **common_analytics_data,
                title=request.data.get("title", ""),
            )

        case Tag.SEARCH:
            city_code = request.data.get("search_city_code", "")
            department = code_insee_to_code_dept(city_code) if city_code else ""
            num_results = int(request.data.get("search_num_results", "0"))
            num_di_results = int(request.data.get("num_di_results", "0"))
            num_di_results_top10 = int(request.data.get("num_di_results_top10", "0"))
            kinds = request.data.get("kinds", [])
            fee_conditions = request.data.get("fee_conditions")
            location_kinds = request.data.get("location_kinds")
            results_slugs_top10 = request.data.get("results_slugs_top10", [])
            event = SearchView.objects.create(
                **common_analytics_data,
                city_code=city_code,
                department=department,
                num_results=num_results,
                num_di_results=num_di_results,
                num_di_results_top10=num_di_results_top10,
                results_slugs_top10=results_slugs_top10,
            )
            cats_values = request.data.get("category_ids", [])
            subcats_values = request.data.get("sub_category_ids", [])
            categories, subcategories = get_categories(cats_values, subcats_values)
            event.categories.set(categories)
            event.subcategories.set(subcategories)
            event.kinds.set(ServiceKind.objects.filter(value__in=kinds))
            event.fee_conditions.set(
                ServiceFee.objects.filter(value__in=fee_conditions)
            )
            event.location_kinds.set(
                LocationKind.objects.filter(value__in=location_kinds)
            )

        case Tag.STRUCTURE:
            event = StructureView.objects.create(
                **common_analytics_data, **structure_data
            )

        case Tag.STRUCTURE_INFOS:
            event = StructureInfosView.objects.create(
                **common_analytics_data, **structure_data
            )

        case Tag.SERVICE:
            event = ServiceView.objects.create(
                **common_analytics_data,
                **structure_data,
                **service_data,
                is_orientable=service.is_orientable() is True,
            )
            event.categories.set(service.categories.all())
            event.subcategories.set(service.subcategories.all())

        case Tag.DI_SERVICE:
            event = DiServiceView.objects.create(
                **common_analytics_data, **di_service_data
            )
            cats_values = request.data.get("di_categories", [])
            subcats_values = request.data.get("di_subcategories", [])
            categories, subcategories = get_categories(cats_values, subcats_values)
            event.categories.set(categories)
            event.subcategories.set(subcategories)

        case Tag.ORIENTATION:
            is_di = not service
            event = OrientationView.objects.create(
                orientation=orientation,
                orientation_status=orientation.status,
                **common_analytics_data,
                **structure_data,
                **service_data,
                is_di=is_di,
                di_structure_name=request.data.get("di_structure_name", ""),
                di_service_id=request.data.get("di_service_id", ""),
                di_service_name=request.data.get("di_service_name", ""),
            )
            if not is_di:
                event.categories.set(service.categories.all())
                event.subcategories.set(service.subcategories.all())

        case Tag.SHARE:
            recipient_email = request.data.get("recipient_email", "")
            recipient_kind = request.data.get("recipient_kind", "")
            is_di = not service
            if is_di:
                event = ServiceShare.objects.create(
                    recipient_email=recipient_email,
                    recipient_kind=recipient_kind,
                    is_structure_member=False,
                    is_structure_admin=False,
                    is_di=True,
                    di_structure_name=request.data.get("di_structure_name", ""),
                    di_service_id=request.data.get("di_service_id", ""),
                    di_service_name=request.data.get("di_service_name", ""),
                    structure_department=request.data.get(
                        "di_structure_department", ""
                    ),
                    structure_source=request.data.get("di_source", ""),
                    search_view=search_view,
                    search_view_id=search_view_id,
                    **common_analytics_data,
                )

                cats_values = request.data.get("di_categories", [])
                subcats_values = request.data.get("di_subcategories", [])
                categories, subcategories = get_categories(cats_values, subcats_values)
                event.categories.set(categories)
                event.subcategories.set(subcategories)
            else:
                event = ServiceShare.objects.create(
                    recipient_email=recipient_email,
                    recipient_kind=recipient_kind,
                    is_di=False,
                    **common_analytics_data,
                    **structure_data,
                    **service_data,
                )
                event.categories.set(service.categories.all())
                event.subcategories.set(service.subcategories.all())

        case Tag.MOBILISATION:
            external_link = request.data.get("external_link")
            event = MobilisationEvent.objects.create(
                external_link=external_link,
                **common_analytics_data,
                **structure_data,
                **service_data,
            )
            event.categories.set(service.categories.all())
            event.subcategories.set(service.subcategories.all())

        case Tag.DI_MOBILISATION:
            external_link = request.data.get("external_link")
            event = DiMobilisationEvent.objects.create(
                external_link=external_link, **common_analytics_data, **di_service_data
            )
            cats_values = request.data.get("di_categories", [])
            subcats_values = request.data.get("di_subcategories", [])
            categories, subcategories = get_categories(cats_values, subcats_values)
            event.categories.set(categories)
            event.subcategories.set(subcategories)

        case _:
            return Response({"error": f"Unknown analytics tag: {tag}"}, status=404)

    return Response({"tag": tag, "event": event.id}, status=201)
