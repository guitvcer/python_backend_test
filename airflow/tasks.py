import requests

from celery import group, shared_task
from django.urls import reverse

from .models import SearchResult
from .services import get_amount


@shared_task
def get_provider_data(app_name: str, base_uri: str, search_id: int):
    """Получить данные с провайдера"""

    provider_url = reverse("{0}:search".format(app_name))
    provider_data = requests.post(base_uri[:-1] + provider_url).json()

    search_result = SearchResult.objects.get(search_id=search_id)
    search_result.amount += get_amount(provider_data)
    search_result.items += provider_data
    search_result.save()


@shared_task
def update_search_result(base_uri: str, search_id: int) -> None:
    """Обновить результат поиска"""

    group(get_provider_data.s(app_name, base_uri, search_id)
          for app_name in ("provider_a", "provider_b"))().get()

    search_result = SearchResult.objects.get(search_id=search_id)
    search_result.status = "C"
    search_result.save()
