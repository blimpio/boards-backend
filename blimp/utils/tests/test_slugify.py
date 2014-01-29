from django.test import TestCase

from blimp.accounts.models import Account
from ..slugify import unique_slugify, _slug_strip


class SlugifyTestCase(TestCase):
    def setUp(self):
        self.acme_account = Account.objects.create(name='Acme')
        self.example_account = Account.objects.create(name='Example')

    def test_unique_slugify_should_set_unique_slug_attr(self):
        """
        Tests that unique_slugify sets the unique slug in the model's
        slug field by default.
        """
        unique_slugify(self.example_account, 'acme')

        self.assertEqual(self.example_account.slug, 'acme-1')

    def test_unique_slugify_should_set_unique_slug_custom_attr(self):
        """
        Tests that unique_slugify sets the unique slug in a custom
        specified model's field.
        """
        unique_slugify(self.example_account, 'acme',
                       slug_field_name='name')

        self.assertEqual(self.example_account.name, 'acme')

    def test_unique_slugify_should_use_slug_separator(self):
        """
        Tests that unique_slugify uses a hyphen as a slug separator.
        """
        unique_slugify(self.example_account, 'acme')

        self.assertEqual(self.example_account.slug.split('-'), ['acme', '1'])

    def test_unique_slugify_should_use_custom_slug_separator(self):
        """
        Tests that unique_slugify can use a custom specified slug separator.
        """
        unique_slugify(self.example_account, 'acme', slug_separator='.')

        self.assertEqual(self.example_account.slug.split('.'), ['acme', '1'])

    def test_slug_strip_should_strip_slug_separators(self):
        """
        Tests that _slug_strip used by unique_slugify removes slug separators
        that occur at the beginnning or end of a slug.
        """
        self.assertEqual(_slug_strip('-my-slug-'), 'my-slug')

    def test_slug_strip_should_strip_custom_slug_separators(self):
        """
        Tests that _slug_strip can use an alternate specified separator.
        """
        self.assertEqual(_slug_strip('@my-@slug%', '@'), 'my@slug%')
