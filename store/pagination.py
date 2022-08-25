from rest_framework.pagination import PageNumberPagination

class PaginationClass(PageNumberPagination):
    page_size = 10