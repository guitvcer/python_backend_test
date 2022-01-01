from django.urls import reverse

from django.views.generic import TemplateView
from rest_framework.generics import get_object_or_404
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView, Response

from .models import SearchResult
from .serializers import SearchResultIdSerializer, SearchResultSerializer
from .tasks import update_search_result


class HomeView(TemplateView):
    """Главная страница"""

    template_name = "airflow/home.html"


class SearchView(APIView):
    """Создает в БД результат поиска и возвращает его id"""

    def post(self, *args, **kwargs):
        search_result = SearchResult.objects.create()
        base_uri = self.request.build_absolute_uri(reverse("airflow:home"))
        update_search_result.delay(base_uri, search_result.search_id)
        serializer = SearchResultIdSerializer(search_result)

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
