import jwt

from django.test import TestCase

from ..models import User, get_user_upload_path


class UserModelTestCase(TestCase):
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

    def test_custom_user_model_should_have_expected_number_of_fields(self):
        """
        Tests the expected number of fields in custom User model.
        """
        expected_fields = 24
        self.assertEqual(len(self.user._meta.fields), expected_fields)

    def test_get_full_name_should_concatenate_names(self):
        """
        Tests that get_full_name returns the user's first name
        plus the last name, with a space in between.
        """
        self.assertEqual(self.user.get_full_name(), 'Juan Pueblo')

    def test_get_short_name_should_return_first_name(self):
        """
        Tests that get_short_name returns the user's first name
        """
        self.assertEqual(self.user.get_short_name(), 'Juan')

    def test_update_last_ip_when_user_logs_in(self):
        """
        TODO: Find a way to test this correctly.
        """
        pass

    def test_user_upload_path_should_have_expected_segments(self):
        """
        Tests that get_user_upload_path returns the expected
        number of segments.
        """
        path = get_user_upload_path(self.user, 'myfile.jpg')
        segments = path.split('/')
        expected_segments = 5

        self.assertEqual(len(segments), expected_segments)

    def test_user_upload_path_should_not_rename_file(self):
        """
        Tests that get_user_upload_path does not rename file name.
        """
        path = get_user_upload_path(self.user, 'myfile.jpg')
        segments = path.split('/')

        self.assertEqual('myfile.jpg', segments[-1])

    def test_user_password_reset_token(self):
        """
        Tests that password_reset_token returns a token that the manager's
        get_from_password_reset_token can use to return a User.
        """
        token = self.user.password_reset_token
        user = User.objects.get_from_password_reset_token(token)

        self.assertEqual(self.user, user)

    def test_user_set_password_changes_token_version(self):
        """
        Tests that set_password set's the user password and
        changes the token_version.
        """
        password = str(self.user.password)
        token_version = str(self.user.token_version)

        self.user.set_password('newpassword')

        self.assertNotEqual(self.user.password, password)
        self.assertNotEqual(self.user.token_version, token_version)
