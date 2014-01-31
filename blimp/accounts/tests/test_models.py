from django.test import TestCase

from blimp.users.models import User
from blimp.invitations.models import InvitedUser
from ..models import (Account, AccountCollaborator, EmailDomain,
                      get_company_upload_path)


class AccountTestCase(TestCase):
    def setUp(self):
        self.username = 'jpueblo'
        self.password = 'abc123'

        self.user = User.objects.create_user(
            username=self.username,
            email='jpueblo@example.com',
            password=self.password,
            first_name='Juan',
            last_name='Pueblo'
        )

        self.account = Account.objects.create(name='Acme')

    def test_create_new_account_sets_unique_slug(self):
        account = Account.objects.create(name='Acme')

        self.assertEqual(account.slug, 'acme-1')

    def test_add_email_domains_should_create_email_domains(self):
        self.account.add_email_domains(['example.com', 'acme.com'])

        self.assertEqual(EmailDomain.objects.count(), 2)

    def test_invite_user_should_return_inviteduser_get_or_create_tuple(self):
        data = {
            'email': 'ppueblo@example.com',
            'role': 'team_member',
            'created_by': self.user
        }

        invited_user_tuple = self.account.invite_user(data)

        invited_user = InvitedUser.objects.get(
            email=data['email'], account=self.account)

        self.assertEqual(invited_user_tuple, (invited_user, True))

    def test_get_company_upload_path_should_have_expected_segments(self):
        """
        Tests that get_company_upload_path returns the expected
        number of segments.
        """
        path = get_company_upload_path(self.account, 'myfile.jpg')
        segments = path.split('/')
        expected_segments = 5

        self.assertEqual(len(segments), expected_segments)

    def test_get_company_upload_path_should_not_rename_file(self):
        """
        Tests that get_company_upload_path does not rename file name.
        """
        path = get_company_upload_path(self.account, 'myfile.jpg')
        segments = path.split('/')

        self.assertEqual('myfile.jpg', segments[-1])


class AccountCollaboratorTestCase(TestCase):
    def setUp(self):
        self.username = 'jpueblo'
        self.password = 'abc123'

        self.user = User.objects.create_user(
            username=self.username,
            email='jpueblo@example.com',
            password=self.password,
            first_name='Juan',
            last_name='Pueblo'
        )

        self.account = Account.objects.create(name='Acme')

    def test_manager_create_owner_should_create_member_with_owner_role(self):
        """
        Tests that manager method create_owner should create
        an AccountMember with the owner role.
        """
        account_member = AccountCollaborator.objects.create_owner(
            account=self.account, user=self.user)

        self.assertTrue(account_member.is_owner)
