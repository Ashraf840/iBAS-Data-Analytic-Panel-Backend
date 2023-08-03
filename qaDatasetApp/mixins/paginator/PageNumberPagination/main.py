from rest_framework.pagination import PageNumberPagination


# [Pagination Motivation]
#  - https://www.django-rest-framework.org/api-guide/pagination/
#  - https://www.sankalpjonna.com/learn-django/pagination-made-easy-with-django-rest-framework
#  - https://www.tomchristie.com/rest-framework-2-docs/api-guide/pagination
#  - https://stackoverflow.com/a/47225624
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
