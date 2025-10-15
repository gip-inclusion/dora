from django.contrib import messages
from django.urls import reverse
from django.utils.html import format_html
from pytest_django.asserts import assertMessages


def test_check_orientation(admin_client, orientation):
    response = admin_client.get(
        reverse(
            "admin:orientations_orientation_change",
            kwargs={"object_id": orientation.pk},
        )
    )
    content = format_html(
        "<p>Cette demande d'orientation comporte des avertissements :</p><p><p>- la structure du prescripteur n&#x27;est pas encore validée</p><p>- le prescripteur s&#x27;est inscrit récemment (moins de 3 semaines)</p><p>- vérifier les informations du prescripteur en ligne : <a href='https://www.google.com/search?q=++{}' target='_blank'>via Google</a></p></p>",
        orientation.prescriber_structure,
    )
    assertMessages(response, [messages.Message(messages.WARNING, content)])
