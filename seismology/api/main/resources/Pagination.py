from sqlalchemy_filters import apply_filters, apply_sort, apply_pagination


class Pagination:
    def __init__(self, query, page_num, elem_per_page):
        self.__query = query
        self.__page_num = page_num
        self.__elem_per_page = elem_per_page

    def __filter(self, value):
        self.__query = apply_filters(self.__query, value)
        return self.__query

    def __sort_by(self, *value):
        self.__query = apply_sort(self.__query, value)
        return self.__query

    def __page(self, value):
        if value >= 1:
            self.__page_num = value
        return self.__query

    def __elem_per_page(self, *value):
        if int(value) >= 1:
            self.__elem_per_page = value
        return self.__query

    def pagination(self):
        return apply_pagination(self.__query, page_number=self.__page_num, page_size=self.__elem_per_page)

    def apply(self, key, value):
        pag_dict = {
            "filter": self.__filter,
            "sort_by": self.__sort_by,
            "page": self.__page,
            "elem_per_page": self.__elem_per_page
        }
        if key in pag_dict.keys():
            return pag_dict[key](value)
        else:
            return self.__query
