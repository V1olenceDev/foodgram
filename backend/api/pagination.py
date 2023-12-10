from rest_framework.pagination import PageNumberPagination


class CustomPaginator(PageNumberPagination):
    """
    Настроенный класс пагинатора,
    который расширяет стандартный PageNumberPagination.
    """
    page_size_query_param = 'limit'
    page_size = 6
