import pytest


@pytest.mark.parametrize(
    "insee_code,expected_name",
    [
        ("75056", "Paris"),
        ("69123", "Lyon"),
        ("2A004", "Ajaccio"),
        ("2a004", "Ajaccio"),
    ],
)
def test_get_city_label_returns_city_name(
    client, test_cities, insee_code, expected_name
):
    """Test que l'endpoint retourne le nom de la ville pour un code INSEE valide."""
    response = client.get(f"/city-label/{insee_code}/")
    assert response.status_code == 200
    assert response.json() == expected_name


@pytest.mark.parametrize(
    "insee_code",
    [
        "99999",
        "0",
    ],
)
def test_get_city_label_returns_404(client, insee_code):
    """Test que l'endpoint retourne 404 pour un code INSEE invalide ou inconnu."""
    response = client.get(f"/city-label/{insee_code}/")
    assert response.status_code == 404
