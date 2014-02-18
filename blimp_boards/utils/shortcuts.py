from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import resolve_url


def redirect_with_params(request, to, *args, **kwargs):
    """
    Returns an HttpResponseRedirect to the appropriate
    URL for the arguments passed. By default issues a temporary
    redirect; pass permanent=True to issue a permanent redirect.

    Copies current request's query paramaters and appends it
    to the resolved URL with any additional params.
    """
    params = kwargs.pop('params', None)
    query_dict = request.GET.copy()

    if kwargs.pop('permanent', False):
        redirect_class = HttpResponsePermanentRedirect
    else:
        redirect_class = HttpResponseRedirect

    if params and isinstance(params, dict):
        query_dict.update(params)

    resolved_url = resolve_url(to, *args, **kwargs)

    if query_dict:
        resolved_url = '{}?{}'.format(
            resolved_url, query_dict.urlencode())

    return redirect_class(resolved_url)
