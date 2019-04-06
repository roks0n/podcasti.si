from django.urls import reverse


def test_health_200(client):
    response = client.get(reverse("health"))
    assert response.status_code == 200
