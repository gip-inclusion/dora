from django.core.management import call_command


def test_notifications_disabled(notifications_disabled, stdout):
    call_command("process_notification_tasks", stdout=stdout)
    result = stdout.getvalue()

    assert (
        "Le système de notification n'est pas activé sur cet environnement." in result
    )


def test_notifications_enabled(notifications_enabled, stdout):
    call_command("process_notification_tasks", stdout=stdout)
    result = stdout.getvalue()

    assert (
        "Le système de notification n'est pas activé sur cet environnement."
        not in result
    )
    assert "les notifications ne sont pas créées dans ce mode" in result


def test_notifications_with_limit(with_limit, stdout):
    call_command("process_notification_tasks", stdout=stdout)
    result = stdout.getvalue()

    assert "limite de notifications par tâche : 10" in result


def test_notifications_with_types(with_types, stdout):
    call_command("process_notification_tasks", stdout=stdout)
    result = stdout.getvalue()

    assert "tâche(s) sélectionnée(s)" in result
    assert "orphan_structures" in result
