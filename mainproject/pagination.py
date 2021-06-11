
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 5


class CustomPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'meta': {
                'last_page': self.page.paginator.count,
                'page': int(self.request.GET.get('page', DEFAULT_PAGE)),
                'page_size': int(self.request.GET.get('page_size', self.page_size)),
                'next':self.get_next_link(),
                'previous':self.get_previous_link()
            }
        })
