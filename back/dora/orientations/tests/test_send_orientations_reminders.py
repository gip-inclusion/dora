from django.core.management import call_command


def test_management_command(caplog, capsys, snapshot):
    call_command("send_orientations_reminders")
    assert caplog.messages[-1].startswith(
        "Management command dora.orientations.management.commands.send_orientations_reminders succeeded in "
    )
    assert caplog.messages[:-1] == snapshot(name="logs")
    assert capsys.readouterr() == snapshot(name="output")
