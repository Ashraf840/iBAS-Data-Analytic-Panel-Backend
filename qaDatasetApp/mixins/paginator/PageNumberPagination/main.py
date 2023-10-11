from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPaginationMixin(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPaginationMixin(PageNumberPagination):
    """
    Return 20 records in a single page & max page number is up to 1000
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000
