import pytest
from django.db import models

from dora.notifications.models import Notification
from dora.structures.models import Structure

from ..core import Task


class FakeTask(Task):
    @classmethod
    def task_type(cls):
        return "fake"

    @classmethod
    def candidates(cls):
        return models.QuerySet(model=Notification)

    @classmethod
    def should_trigger(cls):
        return True

    @classmethod
    def process(cls):
        print("processed fake!")


class StructureTask(Task):
    @classmethod
    def task_type(cls):
        return "generic_task"

    @classmethod
    def candidates(cls):
        # les structures avec un membre ou plus sont considerées comme exclues des candidats
        # ou obsolètes, si changement d'état entre intervenu entre la création de la notification
        # et son exécution
        return Structure.objects.filter(members=None)

    @classmethod
    def should_trigger(cls, notification):
        return notification.counter < 101

    @classmethod
    def process(cls, notification):
        if notification.counter == 42:
            raise Exception("process failed")
        print("processed structure!")

    @classmethod
    def post_process(cls, notification):
        if notification.counter == 43:
            raise Exception("post-process failed")
        print("post-processed structure!")


@pytest.fixture
def fake_task():
    return FakeTask()


@pytest.fixture
def structure_task():
    return StructureTask()
