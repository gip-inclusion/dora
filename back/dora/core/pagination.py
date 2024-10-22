from rest_framework import pagination


class OptionalPageNumberPagination(pagination.PageNumberPagination):
    # La page désirée peut être obtenue avec `?page=X`.
    # Si `page_size` est renseigné dans les paramètres de l'URL,
    # le resultat sera paginé, sinon il restera à plat.

    page_size_query_param = "page_size"

    def get_page_size(self, request):
        if self.page_size_query_param in request.query_params:
            return super().get_page_size(request)
        return None
