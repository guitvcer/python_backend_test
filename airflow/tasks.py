import json
import xmltodict
import requests

from celery import group, shared_task
from django.urls import reverse

from .models import SearchResult
from .services import get_amount, update_currency


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


@shared_task
def load_currencies() -> None:
    """Загрузить валюты и сохранить в БД"""

    print("HELLLLLOOOOOO")

    currencies_xml = requests.get("https://www.nationalbank.kz/rss/get_rates.cfm?fdate=26.10.2021").text
    currencies_json = json.dumps(xmltodict.parse(currencies_xml), ensure_ascii=False)
    currencies = json.loads(currencies_json)

    for currency in currencies["rates"]["item"]:
        update_currency(currency)

    update_currency({
        "fullname": "КАЗАХСТАНСКИЙ ТЕНГЕ",
        "title": "KZT",
        "description": "1",
    })
