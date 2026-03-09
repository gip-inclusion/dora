"""
Synchronise la table django_migrations avec les fichiers de migration présents
sur le disque, sans exécuter les opérations.

À utiliser après une réinitialisation des migrations Django : supprime les entrées
existantes pour les apps dora, puis ré-insère une ligne par fichier de migration
(ordre 0001, 0002, …) avec applied = NOW().
"""

from pathlib import Path

from django.conf import settings
from django.db import connection
from itoutils.django.commands import dry_runnable

from dora.core.commands import BaseCommand


def get_dora_apps_with_migrations():
    """
    Retourne la liste des (app_label, chemin_migrations) pour chaque app
    sous dora/ ayant un répertoire migrations/ avec au moins un fichier .py
    (hors __init__.py).
    """
    apps_dir = getattr(settings, "APPS_DIR", None) or Path(settings.BASE_DIR) / "dora"
    apps_dir = Path(apps_dir)
    if not apps_dir.is_dir():
        return []

    result = []
    for entry in sorted(apps_dir.iterdir()):
        if not entry.is_dir():
            continue
        migrations_dir = entry / "migrations"
        if not migrations_dir.is_dir():
            continue
        py_files = [f for f in migrations_dir.glob("*.py") if f.name != "__init__.py"]
        if not py_files:
            continue
        app_label = entry.name
        result.append((app_label, migrations_dir))
    return result


def get_migration_names_sorted(migrations_dir):
    """
    Retourne la liste des noms de migration (sans .py), triés par numéro
    (0001, 0002, …).
    """
    names = []
    for path in migrations_dir.glob("*.py"):
        if path.name == "__init__.py":
            continue
        names.append(path.stem)
    return sorted(names)


class Command(BaseCommand):
    help = (
        "Synchronise django_migrations avec les fichiers de migration sur disque "
        "(sans exécuter les opérations). À utiliser après un reset des migrations."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--wet-run",
            action="store_true",
            help="Exécute réellement les opérations (sans ce flag, rollback automatique).",
        )

    @dry_runnable
    def handle(self, *args, **options):
        apps = get_dora_apps_with_migrations()

        if not apps:
            self.logger.warning(
                "Aucune app dora avec des migrations trouvée (vérifier APPS_DIR)."
            )
            return

        app_labels = [app_label for app_label, _ in apps]
        self.logger.info("Apps concernées : %s", ", ".join(app_labels))

        with connection.cursor() as cursor:
            placeholders = ", ".join("%s" for _ in app_labels)
            delete_sql = f"DELETE FROM django_migrations WHERE app IN ({placeholders})"
            cursor.execute(delete_sql, app_labels)
            self.logger.info(
                "Supprimé les entrées django_migrations pour %d app(s).",
                len(app_labels),
            )

            insert_sql = (
                "INSERT INTO django_migrations (app, name, applied) "
                "VALUES (%s, %s, NOW())"
            )
            total = 0
            for app_label, migrations_dir in apps:
                for name in get_migration_names_sorted(migrations_dir):
                    cursor.execute(insert_sql, [app_label, name])
                    total += 1

            self.logger.info("Inséré %d entrée(s) dans django_migrations.", total)
