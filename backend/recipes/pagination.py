from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    def __init__(self):
        super().__init__()
        self.page_size_query_param = "limit"
