from django.contrib import messages
from django.urls import reverse
from pytest_django.asserts import assertMessages


def test_check_orientation(admin_client, orientation):
    response = admin_client.get(
        reverse(
            "admin:orientations_orientation_change",
            kwargs={"object_id": orientation.pk},
        )
    )
    content = f"<p>Cette demande d'orientation comporte des avertissements :</p><p><p>- la structure du prescripteur n'est pas encore validée</p><p>- le prescripteur s'est inscrit récemment (moins de 3 semaines)</p><p>- vérifier les informations du prescripteur en ligne : <a href='https://www.google.com/search?q=++{orientation.prescriber_structure}' target='_blank'>via Google</a></p></p>"
    assertMessages(response, [messages.Message(messages.WARNING, content)])
