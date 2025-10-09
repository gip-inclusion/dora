from datetime import datetime, timedelta
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import json
import requests
import os

load_dotenv()


def get_share_services_actions(matomo_base_url, token):
    start_date = datetime.strptime("2025-05-01", "%Y-%m-%d")
    end_date = datetime.today()
    current_date = start_date

    segment = "eventCategory==Page Service;eventAction==Clic Bouton Envoyer la Fiche,eventCategory==Page Service;eventAction==Clic Bouton Partager cette Fiche,eventCategory==Page Service;eventAction==Clic Bouton Profil Professionnel"
    actions = []

    while current_date <= end_date:
        print(f"\t> {current_date}")
        date_str = current_date.strftime("%Y-%m-%d")

        url = (
            f"{matomo_base_url}"
            "?module=API"
            "&method=Live.getLastVisitsDetails"
            f"&idSite=211"
            "&expanded=1"
            "&period=day"
            f"&date={date_str}"
            "&format=json"
            f"&token_auth={token}"
            f"&segment={segment}"
        )

        response = requests.get(url, headers={"Accept": "application/json"})
        try:
            data = response.json()
        except json.JSONDecodeError:
            continue

        event_actions = (
            "Clic Bouton Envoyer la Fiche",
            "Clic Bouton Partager cette Fiche",
            "Clic Bouton Profil Professionnel",
        )
        changement_profil_pro = 0

        for visit in data:
            for event in visit["actionDetails"]:
                if (
                    event["type"] == "event"
                    and event["eventCategory"] == "Page Service"
                    and event["eventAction"] in event_actions
                ):
                    if event["eventAction"] == "Clic Bouton Partager cette Fiche":
                        actions.append(
                            {
                                "visitId": visit["idVisit"],
                                "visitorId": visit["visitorId"],
                                "slug": event["eventName"].split(" ")[0],
                                "envoi_fiche": None,
                                "partage_fiche": 1,
                                "profil_pro": None,
                                "serverdate": event["serverTimePretty"],
                                "date": date_str,
                            }
                        )
                    elif event["eventAction"] == "Clic Bouton Profil Professionnel":
                        changement_profil_pro += 1
                    elif event["eventAction"] == "Clic Bouton Envoyer la Fiche":
                        actions.append(
                            {
                                "visitId": visit["idVisit"],
                                "visitorId": visit["visitorId"],
                                "slug": event["eventName"].split(" ")[0],
                                "envoi_fiche": 1,
                                "partage_fiche": None,
                                "profil_pro": "Bénéficiaire"
                                if changement_profil_pro % 2 == 0
                                else "Pro",
                                "date": date_str,
                                "serverdate": event["serverTimePretty"],
                            }
                        )
                        changement_profil_pro = 0
        current_date += timedelta(days=1)

    return pd.DataFrame(actions)


def push_to_db():
    matomo_base_url = os.getenv("MATOMO_BASE_URL")
    matomo_token = os.getenv("MATOMO_TOKEN")
    database_url = os.getenv("DATABASE_URL").replace("postgres", "postgresql", 1)

    engine = create_engine(database_url)
    print("🔄 Loading data from matomo..")

    table = get_share_services_actions(matomo_base_url, matomo_token)
    print("🔄 Pushing data to database")

    table.to_sql(
        "mtm_share_service_tracking",
        engine,
        schema="matomo",
        if_exists="replace",
        index=False,
    )
    print("✅ Data ready")


push_to_db()
