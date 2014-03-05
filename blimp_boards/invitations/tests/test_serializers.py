from ...utils.tests import BaseTestCase
from ...accounts.models import EmailDomain
from ..models import InvitedUser
from ..serializers import SignupRequestSerializer, InvitedUserSerializer


class SignupRequestSerializerTestCase(BaseTestCase):
    def setUp(self):
        self.email = 'jpueblo@example.com'

        self.data = {
            'email': self.email
        }

    def test_serializer_empty_data(self):
        """
        Tests that serializer.object returns None if no data given.
        """
        serializer = SignupRequestSerializer()
        self.assertEqual(serializer.object, None)

    def test_serializer_validation(self):
        """
        Tests serializer's expected validation errors.
        """
        serializer = SignupRequestSerializer(data={})
        serializer.is_valid()
        expected_errors = {
            'email': ['This field is required.']
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_valid_data(self):
        """
        Tests serializer expected data if valid.
        """
        serializer = SignupRequestSerializer(data=self.data)
        serializer.is_valid()

        self.assertEqual(serializer.data, self.data)


class InvitedUserSerializerTestCase(BaseTestCase):
    def test_serializer_empty_data(self):
        """
        Tests that serializer.object returns None if no data given.
        """
        serializer = InvitedUserSerializer()
        self.assertEqual(serializer.object, None)

    def test_serializer_validation(self):
        """
        Tests serializer's expected validation errors.
        """
        serializer = InvitedUserSerializer(data={})
        serializer.is_valid()
        expected_errors = {
            'account': ['This field is required.'],
            'email': ['This field is required.']
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_valid_data(self):
        """
        Tests serializer expected data if valid.
        """
        self.create_user()
        self.create_account()

        self.account.allow_signup = True
        self.account.save()

        email_domain = EmailDomain.objects.create(domain_name='example.com')
        self.account.email_domains.add(email_domain)

        self.data = {
            'account': self.account.id,
            'email': 'jackson.flores78@example.com'
        }

        serializer = InvitedUserSerializer(data=self.data)
        serializer.is_valid()

        self.assertEqual(serializer.data, self.data)

    def test_serializer_account_validation_error(self):
        """
        Tests serializer validation error when validation account.
        """
        self.create_user()
        self.create_account()

        self.data = {
            'account': self.account.id,
            'email': 'jackson.flores78@example.com'
        }

        serializer = InvitedUserSerializer(data=self.data)
        serializer.is_valid()

        expected_errors = {
            'account': ['Account does not allow signup with email address.']
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_send_invite_should_invite_user(self):
        """
        Tests that serializer.send_invite() should send user invitation.
        """
        self.create_user()
        self.create_account()

        self.account.allow_signup = True
        self.account.save()

        email_domain = EmailDomain.objects.create(domain_name='example.com')
        self.account.email_domains.add(email_domain)

        self.data = {
            'account': self.account.id,
            'email': 'jackson.flores78@example.com'
        }

        serializer = InvitedUserSerializer(data=self.data)
        serializer.is_valid()
        serializer.send_invite()

        invited_users = InvitedUser.objects.all()

        self.assertEqual(invited_users.count(), 1)
