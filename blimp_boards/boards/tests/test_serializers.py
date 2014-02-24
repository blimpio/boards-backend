from rest_framework.test import APIRequestFactory

from ...utils.tests import BaseTestCase
from ..views import BoardViewSet
from ..serializers import BoardSerializer, BoardCollaboratorRequestSerializer


class BoardSerializerTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()
        self.create_account()
        self.create_board()

        self.serializer_class = BoardSerializer
        self.data = {
            'name': 'My Board',
            'account': self.account.id
        }

        self.factory = APIRequestFactory()

    def test_serializer_empty_data(self):
        """
        Tests that serializer.data doesn't return any data.
        """
        serializer = self.serializer_class()
        expected_data = {
            'name': '',
            'account': None,
            'is_shared': False,
            'thumbnail_sm_path': '',
            'thumbnail_md_path': '',
            'thumbnail_lg_path': ''
        }

        self.assertEqual(serializer.data, expected_data)

    def test_serializer_validation(self):
        """
        Tests serializer's expected validation errors.
        """
        serializer = self.serializer_class(data={})
        serializer.is_valid()

        expected_errors = {
            'account': ['This field is required.'],
            'name': ['This field is required.'],
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_should_return_error_if_not_a_collaborator(self):
        self.account_owner.delete()
        request = self.factory.post('/')
        request.user = self.user

        context = {
            'request': request,
            'view': BoardViewSet.as_view()
        }

        serializer = self.serializer_class(data=self.data, context=context)
        serializer.is_valid()

        expected_errors = {
            'account': ['You are not a collaborator in this account.']
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_should_return_object_if_valid(self):
        """
        Tests that serializer should return object if valid.
        """
        request = self.factory.post('/')
        request.user = self.user

        context = {
            'request': request,
            'view': BoardViewSet.as_view()
        }

        serializer = self.serializer_class(data=self.data, context=context)
        serializer.is_valid()
        serializer.save()

        expected_data = {
            'created_by': serializer.object.created_by_id,
            'id': serializer.object.id,
            'date_created': serializer.object.date_created,
            'date_modified': serializer.object.date_modified,
            'name': self.data['name'],
            'slug': serializer.object.slug,
            'account': self.account.id,
            'is_shared': False,
            'thumbnail_sm_path': '',
            'thumbnail_md_path': '',
            'thumbnail_lg_path': ''
        }

        self.assertEqual(serializer.data, expected_data)


class BoardCollaboratorRequestSerializerTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()
        self.create_account()
        self.create_board()

        self.serializer_class = BoardCollaboratorRequestSerializer
        self.data = {
            'email': 'myemail@example.com',
            'board': self.board.id
        }

    def test_serializer_empty_data(self):
        """
        Tests that serializer.data doesn't return any data.
        """
        serializer = self.serializer_class()

        expected_data = {
            'email': '',
            'first_name': '',
            'last_name': '',
            'user': None,
            'board': None,
            'message': ''
        }

        self.assertEqual(serializer.data, expected_data)

    def test_serializer_validation(self):
        """
        Tests serializer's expected validation errors.
        """
        serializer = self.serializer_class(data={})
        serializer.is_valid()

        expected_errors = {
            'email': ['This field is required.'],
            'board': ['This field is required.']
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_should_return_data_if_valid(self):
        """
        Tests that serializer should return data if valid.
        """
        serializer = self.serializer_class(data=self.data)
        serializer.is_valid()
        serializer.save()

        expected_data = {
            'id': serializer.object.id,
            'first_name': '',
            'last_name': '',
            'email': 'myemail@example.com',
            'user': None,
            'board': serializer.object.board_id,
            'message': '',
            'date_created': serializer.object.date_created,
            'date_modified': serializer.object.date_modified,
        }

        self.assertEqual(serializer.data, expected_data)
