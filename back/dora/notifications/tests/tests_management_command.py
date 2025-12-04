from django.core.management import call_command


def test_notifications_disabled(caplog, capsys, snapshot, settings):
    settings.NOTIFICATIONS_ENABLED = False

    call_command("process_notification_tasks")

    assert caplog.messages[-1].startswith(
        "Management command dora.notifications.management.commands.process_notification_tasks succeeded in "
    )
    assert caplog.messages[:-1] == snapshot(name="logs")
    assert capsys.readouterr() == snapshot(name="output")


def test_notifications_enabled(caplog, capsys, snapshot, settings):
    settings.NOTIFICATIONS_ENABLED = True

    call_command("process_notification_tasks")

    assert caplog.messages[-1].startswith(
        "Management command dora.notifications.management.commands.process_notification_tasks succeeded in "
    )
    assert caplog.messages[:-1] == snapshot(name="logs")
    assert capsys.readouterr() == snapshot(name="output")


def test_notifications_with_limit(caplog, capsys, snapshot, settings):
    settings.NOTIFICATIONS_ENABLED = True
    settings.NOTIFICATIONS_LIMIT = 10

    call_command("process_notification_tasks")

    assert caplog.messages[-1].startswith(
        "Management command dora.notifications.management.commands.process_notification_tasks succeeded in "
    )
    assert caplog.messages[:-1] == snapshot(name="logs")
    assert capsys.readouterr() == snapshot(name="output")


def test_notifications_with_types(caplog, capsys, snapshot, settings):
    settings.NOTIFICATIONS_ENABLED = True
    settings.NOTIFICATIONS_TASK_TYPES = "orphan_structures"

    call_command("process_notification_tasks")

    assert caplog.messages[-1].startswith(
        "Management command dora.notifications.management.commands.process_notification_tasks succeeded in "
    )
    assert caplog.messages[:-1] == snapshot(name="logs")
    assert capsys.readouterr() == snapshot(name="output")
