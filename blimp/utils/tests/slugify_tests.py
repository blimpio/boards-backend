from django.test import TestCase

from blimp.accounts.models import Account
from ..slugify import unique_slugify, _slug_strip


class SlugifyTestCase(TestCase):
    def setUp(self):
        self.acme_account = Account.objects.create(name='Acme')
        self.example_account = Account.objects.create(name='Example')

    def test_unique_slugify_should_set_unique_slug_attr(self):
        unique_slugify(self.example_account, 'acme')

        self.assertEqual(self.example_account.slug, 'acme-1')

    def test_unique_slugify_should_set_unique_slug_custom_attr(self):
        unique_slugify(self.example_account, 'acme',
                       slug_field_name='name')

        self.assertEqual(self.example_account.name, 'acme')

    def test_unique_slugify_should_use_slug_separator(self):
        unique_slugify(self.example_account, 'acme')

        self.assertEqual(self.example_account.slug.split('-'), ['acme', '1'])

    def test_unique_slugify_should_use_custom_slug_separator(self):
        unique_slugify(self.example_account, 'acme', slug_separator='.')

        self.assertEqual(self.example_account.slug.split('.'), ['acme', '1'])

    def test_slug_strip_should_strip_slug_separators(self):
        self.assertEqual(_slug_strip('-my-slug-'), 'my-slug')

    def test_slug_strip_should_strip_custom_slug_separators(self):
        self.assertEqual(_slug_strip('@my-@slug%', '@'), 'my@slug%')
