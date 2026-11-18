from dora.core.test_utils import make_orientation
from dora.orientations.models import OrientationStatus


def test_france_travail_number_visibility_by_status(api_client):
    """Test que le numéro France Travail n'est visible que quand l'orientation est validée."""
    orientation = make_orientation(beneficiary_france_travail_number="12345678901")

    # Tester tous les statuts possibles
    test_cases = [
        # (statut, devrait_être_visible, devrait_être_accessible)
        (OrientationStatus.MODERATION_PENDING, False, False),
        (OrientationStatus.MODERATION_REJECTED, False, False),
        (OrientationStatus.PENDING, False, True),
        (OrientationStatus.ACCEPTED, True, True),
        (OrientationStatus.REJECTED, False, True),
    ]

    for status, should_be_visible, should_be_accessible in test_cases:
        orientation.status = status
        orientation.save()

        url = (
            f"/orientations/{orientation.query_id}/?h={orientation.get_query_id_hash()}"
        )
        response = api_client.get(url, follow=True)

        if should_be_accessible:
            assert response.status_code == 200
            if should_be_visible:
                assert (
                    response.data["beneficiary_france_travail_number"] == "12345678901"
                )
            else:
                assert response.data["beneficiary_france_travail_number"] == ""
        else:
            # Les orientations en modération ne sont pas accessibles
            assert response.status_code in [401, 403]
