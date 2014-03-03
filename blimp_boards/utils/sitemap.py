from django.contrib.sitemaps import Sitemap

from ..boards.models import Board


class BoardsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Board.objects.filter(is_shared=False)

    def lastmod(self, obj):
        return obj.date_modified


sitemaps = {
    'boards': BoardsSitemap
}
