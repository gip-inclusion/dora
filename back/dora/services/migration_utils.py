import logging

from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


def extract_subcategories(service):
    return [s["value"] for s in service.subcategories.values()]


def extract_categories(service):
    return [s["value"] for s in service.categories.values()]


def unlink_services_from_category(ServiceCategory, Service, category_value):
    """
    Retire la thématique de tous les services
    """
    category = get_category_by_value(ServiceCategory, category_value)
    if category is None:
        raise ValidationError(
            f"Aucune thématique trouvé avec la value '{category_value}'"
        )

    services = Service.objects.filter(categories=category)
    for service in services:
        service.categories.remove(category)


def unlink_services_from_subcategory(ServiceSubCategory, Service, subcategory_value):
    """
    Retire le besoin de tous les services
    """
    subcategory = get_subcategory_by_value(ServiceSubCategory, subcategory_value)

    if subcategory is None:
        raise ValidationError(
            f"Aucun besoin trouvé avec la value: '{subcategory_value}'"
        )

    services = Service.objects.filter(subcategories=subcategory)
    for service in services:
        service.subcategories.remove(subcategory)


def add_categories_and_subcategories_if_subcategory(
    ServiceCategory,
    ServiceSubCategory,
    Service,
    categories_value_to_add,
    subcategory_value_to_add,
    if_subcategory_value,
):
    """
    Si le service a le besoin `if_subcategory_value`, alors :
        - On lui ajoute toutes les thématiques dans `categories_value_to_add`
        - On lui ajoute toutes les besoins dans `subcategory_value_to_add`
    """
    # On vérifie si toutes les thématiques existent
    categories_to_add_ids = []
    for category_value in categories_value_to_add:
        category = get_category_by_value(ServiceCategory, category_value)
        if category is None:
            raise ValidationError(
                f"Aucune thématique trouvé avec la value '{category_value}'"
            )
        categories_to_add_ids.append(category.id)

    # On vérifie si la if_subcategory existe
    if_subcategory = get_subcategory_by_value(ServiceSubCategory, if_subcategory_value)
    if if_subcategory is None:
        raise ValidationError(
            f"Aucun besoin trouvé avec la value: '{if_subcategory_value}'"
        )

    # On vérifie si tous les besoins existent
    subcategories_to_add_ids = []
    for subcategory_value in subcategory_value_to_add:
        subcategory = get_subcategory_by_value(ServiceSubCategory, subcategory_value)
        if subcategory is None:
            raise ValidationError(
                f"Aucun besoin trouvé avec la value: '{subcategory_value}'"
            )
        subcategories_to_add_ids.append(subcategory.id)

    for service in Service.objects.filter(subcategories=if_subcategory):
        sub_categories = extract_subcategories(service)

        if if_subcategory_value in sub_categories:  # TODO; utile ?
            # Ajout des thématiques
            new_categories_ids = [s["id"] for s in service.categories.values()]
            for id in categories_to_add_ids:
                new_categories_ids.append(id)

            service.categories.set(list(set(new_categories_ids)))

            # Ajout des besoins
            new_subcategories_ids = [s["id"] for s in service.subcategories.values()]
            for id in subcategories_to_add_ids:
                new_subcategories_ids.append(id)

            service.subcategories.set(list(set(new_subcategories_ids)))

            # Sauvegarde
            # TODO: utiliser service.subcategories.set()
            Service.objects.filter(pk=service.pk).first().subcategories.set(
                list(set(new_subcategories_ids))
            )
            Service.objects.filter(pk=service.pk).first().categories.set(
                list(set(new_categories_ids))
            )


def create_category(ServiceCategory, value, label):
    # TODO: check category not exists already
    return ServiceCategory.objects.create(value=value, label=label)


def get_subcategory_by_value(ServiceSubCategory, value):
    return ServiceSubCategory.objects.filter(value=value).first()


def get_category_by_value(ServiceCategory, value):
    return ServiceCategory.objects.filter(value=value).first()


def create_subcategory(ServiceSubCategory, value, label):
    # TODO: check subcategory not exists already
    return ServiceSubCategory.objects.create(value=value, label=label)


def update_subcategory_value_and_label(
    ServiceSubCategory, old_value, new_value, new_label
):
    old_subcategory = get_subcategory_by_value(ServiceSubCategory, old_value)

    # Certains besoins ayant été créés via le back-office, certaines migrations peuvent échouer depuis une BDD vide…
    # Pour éviter cela, on quitte la méthode prématurément sans renvoyer d'erreur
    if old_subcategory is None:
        return

    new_subcategory = get_subcategory_by_value(ServiceSubCategory, new_value)
    if new_subcategory is not None:
        raise ValidationError(f"La value '{new_value}' est déjà utilisée")

    old_subcategory.value = new_value
    old_subcategory.label = new_label
    old_subcategory.save()


def rename_subcategory(ServiceSubCategory, value, new_label):
    subcategory = get_subcategory_by_value(ServiceSubCategory, value)

    # Certains besoins ayant été créés via le back-office, certaines migrations peuvent échouer depuis une BDD vide…
    # Pour éviter cela, on quitte la méthode prématurément sans renvoyer d'erreur
    if subcategory is None:
        return

    subcategory.label = new_label
    subcategory.save()


def update_category_value_and_label(
    ServiceCategory,
    ServiceSubCategory,
    old_value,
    new_value,
    new_label,
    migrate_subcategories=True,
):
    old_category = get_category_by_value(ServiceCategory, old_value)

    # Certaines thématiques ayant été créées via le back-office, certaines migrations peuvent échouer depuis une BDD vide…
    # Pour éviter cela, on quitte la méthode prématurément sans renvoyer d'erreur
    if old_category is None:
        return

    new_category = get_category_by_value(ServiceCategory, new_value)
    if new_category is not None:
        raise ValidationError(f"La value '{new_value}' est déjà utilisée")

    old_category.value = new_value
    old_category.label = new_label
    old_category.save()

    # Migration des besoins associés
    if migrate_subcategories:
        for subcategory in ServiceSubCategory.objects.filter(
            value__startswith=f"{old_value}--"
        ).all():
            subcategory.value = subcategory.value.replace(
                f"{old_value}--", f"{new_value}--"
            )
            subcategory.save()


def replace_subcategory(ServiceSubCategory, Service, from_value, to_value):
    """
    Met à jour tous les services en :
        - retirant le besoin `from_value`
        - ajoutant le besoin `to_value`
    """
    from_subcategory = get_subcategory_by_value(ServiceSubCategory, from_value)
    if from_subcategory is None:
        raise ValidationError(f"Aucun besoin trouvé avec la value: '{from_value}'")

    to_subcategory = get_subcategory_by_value(ServiceSubCategory, to_value)
    if to_subcategory is None:
        raise ValidationError(f"Aucun besoin trouvé avec la value: '{to_value}'")

    # TODO: utiliser `add` et `remove`
    for service in Service.objects.all():
        sub_categories = extract_subcategories(service)

        if from_value in sub_categories:
            new_subcategories_ids = [
                s.get("id")
                for s in service.subcategories.values()
                if s.get("value") != from_value
            ]
            new_subcategories_ids.append(to_subcategory.id)

            Service.objects.filter(pk=service.pk).first().subcategories.set(
                list(set(new_subcategories_ids)),
            )


def delete_subcategory(ServiceSubCategory, value):
    """
    Supprime le besoin de la base de données
    """
    # TODO : vérifier que le besoin n'est plus utilisé
    subcategory = get_subcategory_by_value(ServiceSubCategory, value)
    if subcategory is None:
        raise ValidationError(
            f"Suppression impossible : le besoin '{value}' n'existe pas"
        )
    subcategory.delete()


def delete_category(ServiceCategory, value):
    """
    Supprime la thématique de la base de données
    """
    # TODO : vérifier que la thématique n'est plus utilisée
    category = get_category_by_value(ServiceCategory, value)
    if category is None:
        raise ValidationError(
            f"Suppression impossible: la thématique '{value}' n'existe pas"
        )
    category.delete()


def create_service_kind(ServiceKind, value, label):
    return ServiceKind.objects.create(value=value, label=label)


def update_categories_and_subcategories(
    model, old_category, new_categories, old_subcategory, new_subcategories
):
    """Met à jour les catégories et sous-catégories d'un modèle.

    Gère le cas où le modèle n'a pas de champ 'categories' (ex: SavedSearch).
    """
    # Vérifier si le modèle a un champ 'categories' (ManyToManyField)
    if hasattr(model, "categories"):
        for obj in model.objects.filter(categories=old_category):
            obj.categories.remove(old_category)
            obj.categories.add(*new_categories)

    # Vérifier si le modèle a un champ 'subcategories' (ManyToManyField)
    if hasattr(model, "subcategories"):
        for obj in model.objects.filter(subcategories=old_subcategory):
            obj.subcategories.remove(old_subcategory)
            obj.subcategories.add(*new_subcategories)


def update_saved_search_categories(SavedSearch, old_category, new_categories):
    """Met à jour les SavedSearch avec une nouvelle catégorie.

    Si plusieurs nouvelles catégories remplacent l'ancienne, crée un nouveau
    SavedSearch pour chaque nouvelle catégorie.
    """
    if not new_categories:
        return

    saved_searches_to_update = list(SavedSearch.objects.filter(category=old_category))
    for saved_search in saved_searches_to_update:
        if len(new_categories) == 1:
            # Une seule nouvelle catégorie : mettre à jour l'objet existant
            saved_search.category = new_categories[0]
            saved_search.save()
        else:
            # Plusieurs nouvelles catégories : créer un nouveau SavedSearch pour chaque
            # (sauf la première qui remplace l'ancien)
            saved_search.category = new_categories[0]
            saved_search.save()

            # Créer un nouveau SavedSearch pour chaque catégorie supplémentaire
            for new_category in new_categories[1:]:
                new_saved_search = SavedSearch.objects.create(
                    user=saved_search.user,
                    city_code=saved_search.city_code,
                    city_label=saved_search.city_label,
                    category=new_category,
                    frequency=saved_search.frequency,
                    last_notification_date=saved_search.last_notification_date,
                )
                # Copier les relations ManyToMany
                new_saved_search.subcategories.set(saved_search.subcategories.all())
                new_saved_search.kinds.set(saved_search.kinds.all())
                new_saved_search.fees.set(saved_search.fees.all())
                new_saved_search.location_kinds.set(saved_search.location_kinds.all())
                new_saved_search.funding_labels.set(saved_search.funding_labels.all())


def update_all_models_categories_and_subcategories(
    apps, old_category, new_categories, old_subcategory, new_subcategories
):
    """Met à jour les catégories et sous-catégories pour tous les modèles concernés.

    Récupère automatiquement tous les modèles nécessaires et appelle les fonctions
    de mise à jour appropriées.
    """
    # Récupération des modèles
    Service = apps.get_model("services", "Service")
    ServiceModel = apps.get_model("services", "ServiceModel")
    SavedSearch = apps.get_model("services", "SavedSearch")
    ServiceView = apps.get_model("stats", "ServiceView")
    OrientationView = apps.get_model("stats", "OrientationView")
    ServiceShare = apps.get_model("stats", "ServiceShare")
    MobilisationEvent = apps.get_model("stats", "MobilisationEvent")
    DiServiceView = apps.get_model("stats", "DiServiceView")
    DiMobilisationEvent = apps.get_model("stats", "DiMobilisationEvent")
    SearchView = apps.get_model("stats", "SearchView")

    # Mise à jour de SavedSearch.category (ForeignKey)
    update_saved_search_categories(SavedSearch, old_category, new_categories)

    # Mise à jour de tous les modèles avec categories et subcategories (ManyToManyField)
    models_to_update = [
        Service,
        ServiceModel,
        SavedSearch,
        ServiceView,
        OrientationView,
        ServiceShare,
        MobilisationEvent,
        DiServiceView,
        DiMobilisationEvent,
        SearchView,
    ]
    for model in models_to_update:
        update_categories_and_subcategories(
            model,
            old_category,
            new_categories,
            old_subcategory,
            new_subcategories,
        )
