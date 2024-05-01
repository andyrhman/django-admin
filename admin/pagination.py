# ? https://chat.openai.com/c/ac092099-f5d2-48f0-b5dd-ae604ed39a10
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
import math

class CustomPagination(PageNumberPagination):
    page_size = 5  # Default page size
    page_size_query_param = 'page_size'  # Allow client to override the page size via query parameter
    max_page_size = 100  # Maximum limit of page size

    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset, request, view)
        except NotFound:
            self.page = None
            return []

    def get_paginated_response(self, data):
        if self.page is not None:
            total = self.page.paginator.count
            page = self.page.number
            page_size = self.get_page_size(self.request)
            last_page = math.ceil(total / page_size) if page_size else 0
        else:
            total, page, last_page = 0, 1, 0

        return Response({
            "data": data,
            "meta": {
                "total": total,
                "page": page,
                "last_page": last_page,
            }
        })
