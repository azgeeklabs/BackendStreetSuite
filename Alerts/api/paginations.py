
from rest_framework import pagination


class AlertPAgination(pagination.PageNumberPagination):
    page_size = 20