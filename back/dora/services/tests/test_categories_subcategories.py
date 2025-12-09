import pytest
from data_inclusion.schema.v0 import Thematique as ThematiqueV0
from data_inclusion.schema.v1 import Thematique as ThematiqueV1
from model_bakery import baker

from dora.core.utils import get_category_from_subcategory
from dora.services.models import ServiceCategory, ServiceSubCategory


@pytest.mark.parametrize("model_class", [ServiceCategory, ServiceSubCategory])
class TestCategorySubCategoryFiltering:
    """Tests pour le filtrage du queryset sur is_obsolete, mutualisés pour ServiceCategory et ServiceSubCategory."""

    def test_default_manager_excludes_obsolete(self, model_class):
        """Le manager par défaut doit exclure les éléments obsolètes."""
        model_name = model_class.__name__
        active_item = baker.make(
            model_name, value="active", label="Active", is_obsolete=False
        )
        obsolete_item = baker.make(
            model_name, value="obsolete", label="Obsolete", is_obsolete=True
        )

        items = model_class.objects.all()
        # Vérifier que l'élément actif est présent et l'obsolète est absent
        assert active_item in items
        assert obsolete_item not in items

    def test_default_manager_includes_non_obsolete(self, model_class):
        """Le manager par défaut doit inclure les éléments non obsolètes."""
        model_name = model_class.__name__
        item1 = baker.make(model_name, value="item1", label="Item 1", is_obsolete=False)
        item2 = baker.make(model_name, value="item2", label="Item 2", is_obsolete=False)

        items = model_class.objects.all()
        # Vérifier que les deux éléments non obsolètes sont présents
        assert item1 in items
        assert item2 in items

    def test_base_manager_includes_all(self, model_class):
        """Le _base_manager doit inclure tous les éléments, y compris les obsolètes."""
        model_name = model_class.__name__
        active_item = baker.make(
            model_name, value="active", label="Active", is_obsolete=False
        )
        obsolete_item = baker.make(
            model_name, value="obsolete", label="Obsolete", is_obsolete=True
        )

        all_items = model_class._base_manager.all()
        # Vérifier que les deux éléments (actif et obsolète) sont présents dans le _base_manager
        assert active_item in all_items
        assert obsolete_item in all_items

    def test_filter_on_obsolete_field(self, model_class):
        """Le filtrage explicite sur is_obsolete doit fonctionner."""
        model_name = model_class.__name__
        active1 = baker.make(
            model_name, value="active1", label="Active 1", is_obsolete=False
        )
        active2 = baker.make(
            model_name, value="active2", label="Active 2", is_obsolete=False
        )
        obsolete1 = baker.make(
            model_name, value="obsolete1", label="Obsolete 1", is_obsolete=True
        )

        active_items = model_class._base_manager.filter(is_obsolete=False)
        # Vérifier que les éléments actifs sont présents et l'obsolète est absent
        assert active1 in active_items
        assert active2 in active_items
        assert obsolete1 not in active_items

        obsolete_items = model_class._base_manager.filter(is_obsolete=True)
        # Vérifier que l'élément obsolète est présent et les actifs sont absents
        assert obsolete1 in obsolete_items
        assert active1 not in obsolete_items
        assert active2 not in obsolete_items


class TestThematiquesObsolescence:
    """Tests pour vérifier l'obsolescence des thématiques selon les schémas data_inclusion."""

    def test_thematiques_v1_are_not_obsolete(self):
        """Les thématiques de data_inclusion.schema.v1 ne doivent pas être obsolètes."""
        for thematique in ThematiqueV1:
            subcategory = ServiceSubCategory._base_manager.filter(
                value=thematique.value
            ).first()
            if subcategory is not None:
                assert not subcategory.is_obsolete, (
                    f"La thématique v1 '{thematique.value}' ne doit pas être obsolète"
                )

    def test_thematiques_v0_not_in_v1_are_obsolete(self):
        """Les thématiques de data_inclusion.schema.v0 qui ne sont pas dans v1 doivent être obsolètes."""
        v0_values = {thematique.value for thematique in ThematiqueV0}
        v1_values = {thematique.value for thematique in ThematiqueV1}

        v0_only_values = v0_values - v1_values

        for thematique_value in v0_only_values:
            subcategory = ServiceSubCategory._base_manager.filter(
                value=thematique_value
            ).first()
            if subcategory is not None:
                assert subcategory.is_obsolete, (
                    f"La thématique v0 '{thematique_value}' (non présente dans v1) doit être obsolète"
                )

    def test_categories_from_v1_thematiques_are_not_obsolete(self):
        """Les catégories correspondant aux thématiques v1 ne doivent pas être obsolètes."""
        v1_category_values = {
            get_category_from_subcategory(thematique.value)
            for thematique in ThematiqueV1
        }

        for category_value in v1_category_values:
            category = ServiceCategory._base_manager.filter(
                value=category_value
            ).first()
            if category is not None:
                assert not category.is_obsolete, (
                    f"La catégorie '{category_value}' (utilisée dans v1) ne doit pas être obsolète"
                )

    def test_categories_from_v0_not_in_v1_are_obsolete(self):
        """Les catégories des thématiques v0 qui ne sont pas dans v1 doivent être obsolètes."""
        v0_category_values = {
            get_category_from_subcategory(thematique.value)
            for thematique in ThematiqueV0
        }
        v1_category_values = {
            get_category_from_subcategory(thematique.value)
            for thematique in ThematiqueV1
        }

        v0_only_category_values = v0_category_values - v1_category_values

        for category_value in v0_only_category_values:
            category = ServiceCategory._base_manager.filter(
                value=category_value
            ).first()
            if category is not None:
                assert category.is_obsolete, (
                    f"La catégorie '{category_value}' "
                    "(utilisée uniquement par des thématiques v0 non présentes dans v1) "
                    "doit être obsolète"
                )
