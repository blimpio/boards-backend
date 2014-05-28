from rest_framework.test import APIRequestFactory

from ...utils.tests import BaseTestCase
from ..views import CardViewSet
from ..models import Card
from ..serializers import (CardSerializer, StackSerializer,
                           CardCommentSerializer)


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
            'position': -1,
            'featured': False,
            'origin_url': '',
            'content': '',
            'is_shared': False,
            'file_size': 0,
            'mime_type': '',
            'metadata': '',
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
            'created_by': serializer.data['created_by'],
            'modified_by': serializer.data['modified_by'],
            'id': serializer.object.id,
            'position': serializer.object.position,
            'date_created': serializer.object.date_created,
            'date_modified': serializer.object.date_modified,
            'name': self.data['name'],
            'slug': serializer.object.slug,
            'type': self.data['type'],
            'board': self.data['board'],
            'stack': None,
            'cards': [],
            'featured': False,
            'origin_url': serializer.object.origin_url,
            'content': self.data['content'],
            'is_shared': False,
            'thumbnail_xs_path': serializer.object.thumbnail_xs_path,
            'thumbnail_sm_path': serializer.object.thumbnail_sm_path,
            'thumbnail_md_path': serializer.object.thumbnail_md_path,
            'thumbnail_lg_path': serializer.object.thumbnail_lg_path,
            'file_size': None,
            'mime_type': serializer.object.origin_url,
            'html_url': serializer.object.html_url,
            'download_html_url': serializer.object.download_html_url,
            'original_html_url': serializer.object.original_html_url,
            'metadata': serializer.object.metadata,
            'comments_count': serializer.object.comments_count,
        }

        self.assertEqual(serializer.data, expected_data)

    def test_serializer_should_return_object_if_valid_for_card_stack(self):
        """
        Tests that serializer should return object for
        card stack if valid.
        """
        request = self.factory.post('/')
        request.user = self.user

        context = {
            'request': request,
            'view': CardViewSet.as_view()
        }

        card = Card.objects.create(
            name='A Note', type='note', content='abc123',
            board=self.board, created_by=self.user)

        data = {
            'name': 'My Card Stack',
            'type': 'stack',
            'board': self.board.id,
            'cards': [card.id]
        }

        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid()
        serializer.save()

        expected_data = {
            'created_by': serializer.data['created_by'],
            'modified_by': serializer.data['modified_by'],
            'id': serializer.object.id,
            'position': serializer.object.position,
            'date_created': serializer.object.date_created,
            'date_modified': serializer.object.date_modified,
            'name': data['name'],
            'slug': serializer.object.slug,
            'type': data['type'],
            'board': data['board'],
            'cards': [card.id],
            'stack': None,
            'featured': False,
            'origin_url': serializer.object.origin_url,
            'content': serializer.object.content,
            'is_shared': False,
            'thumbnail_xs_path': serializer.object.thumbnail_xs_path,
            'thumbnail_sm_path': serializer.object.thumbnail_sm_path,
            'thumbnail_md_path': serializer.object.thumbnail_md_path,
            'thumbnail_lg_path': serializer.object.thumbnail_lg_path,
            'file_size': None,
            'mime_type': serializer.object.mime_type,
            'html_url': serializer.object.html_url,
            'download_html_url': serializer.object.download_html_url,
            'original_html_url': serializer.object.original_html_url,
            'metadata': serializer.object.data,
            'comments_count': serializer.object.comments_count,
        }

        self.assertEqual(serializer.data, expected_data)


class StackSerializerTestCase(BaseTestCase):
    def setUp(self):
        self.create_user()
        self.create_account()
        self.create_board()
        self.create_card()

        self.serializer_class = StackSerializer
        self.data = {
            'name': 'My Stack',
            'type': 'stack',
            'board': self.board.id,
            'cards': [self.card.id]
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
            'position': -1,
            'board': None,
            'cards': [],
            'featured': False,
            'is_shared': False
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
            'board': ['This field is required.']
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
            'created_by': serializer.data['created_by'],
            'modified_by': serializer.data['modified_by'],
            'id': serializer.object.id,
            'position': serializer.object.position,
            'date_created': serializer.object.date_created,
            'date_modified': serializer.object.date_modified,
            'name': self.data['name'],
            'slug': serializer.object.slug,
            'type': self.data['type'],
            'board': self.data['board'],
            'cards': self.data['cards'],
            'featured': False,
            'is_shared': False,
            'html_url': serializer.object.html_url
        }

        self.assertEqual(serializer.data, expected_data)

    def test_validate_cards_card_type(self):
        """
        Tests that serializer's `.validate_cards` only validates
        if card is not stack and resets cards field to empty list.
        """
        request = self.factory.post('/')
        request.user = self.user

        context = {
            'request': request,
            'view': CardViewSet.as_view()
        }

        card = Card.objects.create(
            name='A new Card', type='note', content='abc123',
            board=self.board, created_by=self.user)

        data = {
            'name': 'My Card Stack',
            'type': 'stack',
            'board': self.board.id,
            'cards': [card.id]
        }

        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid()
        serializer.save()

        expected_data = {
            'created_by': serializer.data['created_by'],
            'modified_by': serializer.data['modified_by'],
            'id': serializer.object.id,
            'position': serializer.object.position,
            'date_created': serializer.object.date_created,
            'date_modified': serializer.object.date_modified,
            'name': data['name'],
            'slug': serializer.object.slug,
            'type': data['type'],
            'board': data['board'],
            'cards': data['cards'],
            'featured': False,
            'is_shared': False,
            'html_url': serializer.object.html_url,
        }

        self.assertEqual(serializer.data, expected_data)

    def test_validate_cards_should_allow_cards_user_can_access(self):
        """
        Tests that serializer's `.validate_cards` validates
        that each card can be accessed by the user.
        """
        request = self.factory.post('/')
        request.user = self.user

        context = {
            'request': request,
            'view': CardViewSet.as_view()
        }

        self.board_collaborator.delete()

        card = Card.objects.create(
            name='A Stack', type='stack',
            board=self.board, created_by=self.user)

        data = {
            'name': 'My Card Stack',
            'type': 'stack',
            'board': self.board.id,
            'cards': [card.id]
        }

        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid()

        expected_errors = {
            'cards': ['Invalid value.']
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_validate_cards_shouldnt_add_stack(self):
        """
        Tests that serializer's `.validate_cards` validates
        each type of the cards attached to it.
        """
        request = self.factory.post('/')
        request.user = self.user

        context = {
            'request': request,
            'view': CardViewSet.as_view()
        }

        card = Card.objects.create(
            name='A Stack', type='stack',
            board=self.board, created_by=self.user)

        data = {
            'name': 'My Card Stack',
            'type': 'stack',
            'board': self.board.id,
            'cards': [card.id]
        }

        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid()

        expected_errors = {
            'cards': ['Invalid value.']
        }

        self.assertEqual(serializer.errors, expected_errors)


class CardCommentSerializerTestCase(BaseTestCase):
    def setUp(self):
        self.serializer_class = CardCommentSerializer
        self.data = {
            'content': 'A comment'
        }

        self.factory = APIRequestFactory()

    def test_serializer_empty_data(self):
        """
        Tests that serializer.data doesn't return any data.
        """
        serializer = self.serializer_class()
        expected_data = {
            'content': '',
        }

        self.assertEqual(serializer.data, expected_data)

    def test_serializer_validation(self):
        """
        Tests serializer's expected validation errors.
        """
        serializer = self.serializer_class(data={})
        serializer.is_valid()

        expected_errors = {
            'content': ['This field is required.']
        }

        self.assertEqual(serializer.errors, expected_errors)

    def test_serializer_should_return_object_if_valid(self):
        """
        Tests that serializer should return object if valid.
        """
        self.create_user()
        self.create_account()
        self.create_board()
        self.create_card()

        request = self.factory.post('/')
        request.user = self.user

        context = {
            'request': request,
            'view': CardViewSet.as_view(),
            'content_object': self.card
        }

        serializer = self.serializer_class(data=self.data, context=context)
        serializer.is_valid()
        serializer.save()

        expected_data = {
            'id': serializer.object.id,
            'content': 'A comment',
            'created_by': self.user.id,
            'modified_by': self.user.id,
            'date_created': serializer.object.date_created,
            'date_modified': serializer.object.date_modified
        }

        self.assertEqual(serializer.data, expected_data)
