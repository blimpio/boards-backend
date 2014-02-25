from rest_framework.response import Response


class ErrorResponse(Response):
    """
    An HttpResponse that renders data into an error dictionary.
    """
    def __init__(self, data=None, status=400, **kwargs):
        data = {
            'error': data
        }

        super(ErrorResponse, self).__init__(data=data, status=status, **kwargs)
