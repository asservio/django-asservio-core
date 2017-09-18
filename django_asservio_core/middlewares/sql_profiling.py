from django.db import connection
from django.conf import settings

from ..utils import terminal_width


class SqlProfilingMiddleware(object):
    """Middleware which prints out a list of all SQL queries done for
        each view that is processed. This is only useful for debugging.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        indentation = 2
        if settings.DEBUG and len(connection.queries) > 0:
            width = terminal_width()
            total_time = 0.0
            for query in connection.queries:
                nice_sql = query['sql'].replace('"', '').replace(',', ', ')
                sql = "Query: %s\nTime: %s" % (nice_sql, query['time'])
                total_time = total_time + float(query['time'])
                while len(sql) > width-indentation:
                    print("%s%s" % (" "*indentation, sql[:width-indentation]))
                    sql = sql[width-indentation:]
                print("%s%s\n" % (" "*indentation, sql))
            total_info = (" "*indentation, str(total_time),
                          len(connection.queries))
            print("%sTotal time: %s seconds. Queries: %s." % total_info)
        return response
