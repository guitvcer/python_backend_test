import json
import requests
import xmltodict
from django.urls import reverse
from typing import Callable
from .models import Currency, SearchResult
from .serializers import CurrencySerializer


def update_currency(currency: dict) -> None:
    """Обновить валюту"""

    serializer = CurrencySerializer(data=currency)

    if serializer.is_valid():
        serializer.save()


def load_currencies() -> None:
    """Загрузить валюты и сохранить в БД"""

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


def get_amount(provider_data: list) -> float:
    """Получить сумму в EUR"""

    amount = 0

    for ticket in provider_data:
        total = float(ticket["pricing"]["total"])
        currency = ticket["pricing"]["currency"]
        amount += Currency.translate_currency(total, currency, "EUR")

    return amount


def update_search_result(
    build_absolute_uri: Callable,
    search_result: SearchResult
) -> None:
    """Обновить результат поиска"""

    search_result.items = []

    for app_name in ("provider_a", "provider_b"):
        provider_url = build_absolute_uri(reverse("{0}:search".format(app_name)))
        provider_data = requests.post(provider_url).json()
        search_result.amount += get_amount(provider_data)
        search_result.items += provider_data

    search_result.status = "C"
    search_result.save()
