from dora.users.models import User

UNNORMALIZED_EMAIL_ADDRESS = "Foo.Bar@Example.Com"
NORMALIZED_EMAIL_ADDREESS = "foo.bar@example.com"


def test_normalize_email():
    assert (
        User.objects.normalize_email(UNNORMALIZED_EMAIL_ADDRESS)
        == NORMALIZED_EMAIL_ADDREESS
    )


def test_create_user():
    user = User.objects.create_user(UNNORMALIZED_EMAIL_ADDRESS)
    assert user.email == NORMALIZED_EMAIL_ADDREESS
