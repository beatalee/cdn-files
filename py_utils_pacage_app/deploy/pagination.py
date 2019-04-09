from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

# https://www.django-rest-framework.org/api-guide/pagination/
class MyPageNumberPagination(PageNumberPagination):
    page_size=2  #默认两个
    page_size_query_param = 'size'  #传一个size参数 一页显示多少  http://127.0.0.1:8000/pager1/?page=1&size=3
    max_page_size = 5  #一页显示最大5个
    page_query_param = 'page'  #页码


class LargeResultsSetPagination(PageNumberPagination):
    max_page_size = 200
    page_size = 1000
    page_size_query_param = 'page_size'


class MyPagenumber2Pagination(LimitOffsetPagination):
    default_limit = 3
    limit_query_param = 'limit'  #每页多少条数据
    offset_query_param = 'offset'  #第几个索引开始
    max_limit = 5


class ShowAllPaginationLimit100(PageNumberPagination):
    max_page_size = 200
    page_size = 1000
    page_size_query_param = 'page_size'