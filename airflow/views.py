from django.views.generic import TemplateView
from multiprocessing import Process

from rest_framework.generics import get_object_or_404
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView, Response
from .models import SearchResult
from .serializers import SearchResultIdSerializer, SearchResultSerializer
from .services import update_search_result


class HomeView(TemplateView):
    """Главная страница"""

    template_name = "airflow/home.html"


class SearchView(APIView):
    """Создает в БД результат поиска и возвращает его id"""

    def post(self, *args, **kwargs):
        search_result = SearchResult.objects.create()
        serializer = SearchResultIdSerializer(search_result)

        p = Process(target=update_search_result, args=(self.request.build_absolute_uri, search_result))
        p.start()

        return Response(serializer.data, status=HTTP_200_OK)


class SearchResultView(APIView):
    """Информация о результате поиска"""

    @staticmethod
    def get(*args, **kwargs):
        search_result = get_object_or_404(SearchResult.objects.all(), search_id=kwargs["search_id"])
        serializer = SearchResultSerializer(search_result, context={
            "currency": kwargs["currency"],
        })

        return Response(serializer.data, status=HTTP_200_OK)
