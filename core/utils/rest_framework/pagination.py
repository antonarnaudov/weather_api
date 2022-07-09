from rest_framework.pagination import PageNumberPagination


class PageSizeNumberPagination(PageNumberPagination):
    """
    Override CursorPagination to use size as query param
    """
    page_size_query_param = 'size'  # items per page
