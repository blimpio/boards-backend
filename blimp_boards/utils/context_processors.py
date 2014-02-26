from django.conf import settings


def app_settings(request):
    return {'settings': settings}
