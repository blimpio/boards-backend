from django import template
from django.conf import settings
from django.utils.six.moves.urllib.parse import urljoin


register = template.Library()


@register.simple_tag(takes_context=True)
def boards_web_static(context, path):
    if settings.ENVIRONMENT != 'DEVELOPMENT':
        request = context['request']

        boards_web_client_version = settings.BOARDS_WEB_CLIENT_VERSION
        client_version = request.GET.get(
            'clientVersion', boards_web_client_version)

        path = '/{}/{}'.format(client_version, path)

    return urljoin(settings.BOARDS_WEB_STATIC_URL, path)
