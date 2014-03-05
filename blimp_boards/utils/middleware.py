from django.db import connection


class QueryCountDebugMiddleware(object):
    """
    From: https://gist.github.com/j4mie/956843

    This middleware adds two headers to the response:
    X-Debug-Query-Count and X-Debug-Query-Duration.
    This headers contain the number of queries run and the total
    time taken for each request (with a status code of 200).
    """
    def process_response(self, request, response):
        if response.status_code == 200:
            total_time = 0

            for query in connection.queries:
                query_time = query.get('time')
                if query_time is None:
                    query_time = query.get('duration', 0) / 1000
                total_time += float(query_time)

            response['X-Debug-Query-Count'] = len(connection.queries)
            response['X-Debug-Query-Duration'] = total_time

        return response
