from rest_framework.test import APIRequestFactory

from ...utils.tests import BaseTestCase
from ..serializers import CardSerializer
from ..views import CardViewSet


class CardSerializerTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()
        self.create_account()
        self.create_board()

        self.serializer_class = CardSerializer
        self.data = {
            'name': 'My Card',
            'type': 'note',
            'board': self.board.id,
            'content': 'My content'
        }

        self.factory = APIRequestFactory()

    def test_serializer_empty_data(self):
        """
        Tests that serializer.data doesn't return any data.
        """
        serializer = self.serializer_class()
        expected_data = {
            'name': '',
            'type': '',
            'board': None,
            'cards': [],
            'featured': False,
            'origin_url': '',
            'content': '',
            'is_shared': False,
            'thumbnail_sm_path': '',
            'thumbnail_md_path': '',
            'thumbnail_lg_path': '',
            'file_size': 0,
            'file_extension': ''
        }

        self.assertEqual(serializer.data, expected_data)

    def test_serializer_validation(self):
        """
        Tests serializer's expected validation errors.
        """
        serializer = self.serializer_class(data={})
        serializer.is_valid()

        expected_errors = {
            'type': ['This field is required.'],
            'name': ['This field is required.'],
            'board': ['This field is required.'],
            'content': ['This field is required.']
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
            'view': CardViewSet.as_view()
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
            'type': self.data['type'],
            'board': self.data['board'],
            'cards': [],
            'featured': False,
            'origin_url': '',
            'content': self.data['content'],
            'is_shared': False,
            'thumbnail_sm_path': '',
            'thumbnail_md_path': '',
            'thumbnail_lg_path': '',
            'file_size': None,
            'file_extension': ''
        }

        self.assertEqual(serializer.data, expected_data)
