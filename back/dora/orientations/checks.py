import logging
from difflib import SequenceMatcher

from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.utils.html import format_html, format_html_join
from django.utils.http import urlencode

from dora.core.models import ModerationStatus

from .models import Orientation

"""
Sécurité : vérifications de conformité de l'orientation

Si des anomalies concernant la validité de l'orientation sont trouvées,
un rapport est généré (sous forme de `list` contenant les avertissements),
qui peut être utilisé dans l'admin sous forme de message,
lors de l'ouverture de l'orientation, par ex.

Les différentes vérifications sont implémentées sous la forme de fonctions `check_...`
qui prennent en paramètre l'objet `Orientation` à tester.
"""

logger = logging.getLogger(__name__)


def check_test(orientation: Orientation) -> list:
    # vérifie la présence de la chaine 'test' dans certain champs (arrive souvent)
    result = []

    test_fields = [
        "beneficiary_last_name",
        "beneficiary_first_name",
        "beneficiary_email",
    ]

    for field_name in test_fields:
        field_value = getattr(orientation, field_name)
        if "test" in field_value.lower():
            result.append(
                f"chaîne de caractère 'test' dans le champ '{Orientation._meta.get_field(field_name).verbose_name}'"
            )

    return result


def check_similar_fields(orientation: Orientation) -> list:
    result = []
    k = 0.75

    if orientation.prescriber:
        matcher = SequenceMatcher(
            None, orientation.prescriber.email, orientation.beneficiary_email
        )
        if matcher.ratio() > k:
            result.append(
                "les adresses e-mail du prescripteur et du bénéficiaire sont similaires"
            )

        matcher.set_seqs(
            orientation.prescriber.last_name, orientation.beneficiary_last_name
        )
        if matcher.ratio() > k:
            result.append("les noms du prescripteur et du bénéficiaire sont similaires")

        ...

    return result


def check_structure(orientation: Orientation) -> list:
    result = []

    if orientation.service:
        # note : dans ce cas, plus optimisé que de passer par structure.is_member
        if (
            orientation.prescriber
            and orientation.prescriber in orientation.service.structure.members.all()
        ):
            result.append(
                "le prescripteur est membre de la structure proposant le service"
            )

        if orientation.service.structure == orientation.prescriber_structure:
            result.append(
                "la structure proposant le service est la même que celle du prescripteur"
            )

    ...

    return result


def check_prescriber(orientation: Orientation) -> list:
    result = []

    if not orientation.prescriber:
        result.append("le prescripteur n'est pas renseigné")

    if orientation.prescriber_structure:
        if (
            orientation.prescriber_structure.moderation_status
            != ModerationStatus.VALIDATED
        ):
            result.append("la structure du prescripteur n'est pas encore validée")

        # note : dans ce cas, plus optimisé que de passer par structure.is_admin
        if (
            orientation.prescriber_structure.membership.count() == 1
            and orientation.prescriber in orientation.prescriber_structure.admins
        ):
            result.append(
                "le prescripteur est le seul membre et administrateur de la structure"
            )

    if (
        orientation.prescriber
        and orientation.prescriber.date_joined > timezone.now() - relativedelta(weeks=3)
    ):
        result.append("le prescripteur s'est inscrit récemment (moins de 3 semaines)")

    if result and orientation.prescriber:
        q = urlencode(
            {
                "q": f"{orientation.prescriber.first_name} {orientation.prescriber.last_name} {orientation.prescriber_structure}"
            }
        )
        result.append(
            format_html(
                "vérifier les informations du prescripteur en ligne : <a href='{}' target='_blank'>via Google</a>",
                "https://www.google.com/search?" + q,
            )
        )

    return result


def check_orientation(orientation: Orientation) -> list | None:
    try:
        msgs = [
            t(orientation)
            for t in [
                check_structure,
                check_prescriber,
                check_test,
                check_similar_fields,
            ]
        ]
        msgs = [f"{msg}" for result in msgs for msg in result]
        return msgs
    except Orientation.DoesNotExist:
        pass
    except Exception as ex:
        msg = f"erreur lors de la vérification de l'orientation {orientation.pk}"
        logger.exception(msg, ex)
        return [msg]

    return None


def format_warnings(warnings: list) -> str:
    return format_html(
        "<p>Cette demande d'orientation comporte des avertissements :</p><p>{}</p>",
        format_html_join("", "<p>- {}</p>", ((w,) for w in warnings)),
    )
