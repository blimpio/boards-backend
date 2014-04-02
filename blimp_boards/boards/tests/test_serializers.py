from rest_framework.test import APIRequestFactory

from ...utils.tests import BaseTestCase
from ...accounts.models import AccountCollaborator
from ..views import BoardViewSet, BoardCollaboratorViewSet
from ..serializers import (BoardSerializer, BoardCollaboratorSerializer,
                           BoardCollaboratorRequestSerializer)


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
            'disqus_shortname': '',
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
            'disqus_shortname': '',
            'thumbnail_sm_path': '',
            'thumbnail_md_path': '',
            'thumbnail_lg_path': ''
        }

        self.assertEqual(serializer.data, expected_data)


class BoardCollaboratorSerializerTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()
        self.create_account()
        self.create_board()

        self.serializer_class = BoardCollaboratorSerializer
        self.data = {
            'board': self.board.id,
            'user': None,
            'invited_user': None,
            'email': 'otheruser@example.com',
            'permission': 'read'
        }

        self.factory = APIRequestFactory()

    def test_serializer_empty_data(self):
        """
        Tests that serializer.data doesn't return any data.
        """
        serializer = self.serializer_class()
        expected_data = {
            'board': None,
            'user': None,
            'invited_user': None,
            'permission': ''
        }

        self.assertEqual(serializer.data, expected_data)

    def test_serializer_validation(self):
        """
        Tests serializer's expected validation errors.
        """
        serializer = self.serializer_class(data={})
        serializer.is_valid()

        expected_errors = {
            'board': ['This field is required.'],
            'permission': ['This field is required.'],
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
            'view': BoardCollaboratorViewSet.as_view()
        }

        serializer = self.serializer_class(data=self.data, context=context)
        serializer.is_valid()
        serializer.save()

        expected_data = {
            'board': serializer.object.board_id,
            'id': serializer.object.id,
            'date_created': serializer.object.date_created,
            'date_modified': serializer.object.date_modified,
            'user': None,
            'invited_user': {
                'id': serializer.object.invited_user_id,
                'first_name': serializer.object.invited_user.first_name,
                'last_name': serializer.object.invited_user.last_name,
                'email': serializer.object.invited_user.email,
                'date_created': serializer.object.invited_user.date_created,
                'date_modified': serializer.object.invited_user.date_modified
            },
            'permission': serializer.object.permission
        }

        self.assertEqual(serializer.data, expected_data)

    def test_serializer_should_set_invited_user_from_email(self):
        """
        Tests that seriazer should set invited_user from email.
        """
        request = self.factory.post('/')
        request.user = self.user

        context = {
            'request': request,
            'view': BoardCollaboratorViewSet.as_view()
        }

        serializer = self.serializer_class(data=self.data, context=context)
        serializer.is_valid()
        serializer.save()

        self.assertEqual(serializer.object.user, None)
        self.assertEqual(serializer.object.invited_user.email,
                         self.data['email'])

    def test_serializer_should_set_user_from_email(self):
        """
        Tests that seriazer should set user from email if an
        account collaborator with that email already exists.
        """
        user = self.create_another_user()

        AccountCollaborator.objects.create(account=self.account, user=user)

        request = self.factory.post('/')
        request.user = self.user

        context = {
            'request': request,
            'view': BoardCollaboratorViewSet.as_view()
        }

        self.data['email'] = user.email

        serializer = self.serializer_class(data=self.data, context=context)
        serializer.is_valid()
        serializer.save()

        self.assertEqual(serializer.object.user, user)
        self.assertEqual(serializer.object.invited_user, None)


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
