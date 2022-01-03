import asyncio
import os
import requests

from asgiref.sync import sync_to_async
from django.urls import reverse

from .models import Currency, SearchResult
from .serializers import CurrencySerializer


def update_currency(currency: dict) -> None:
    """Обновить валюту"""

    serializer = CurrencySerializer(data=currency)

    if serializer.is_valid():
        serializer.save()


def get_amount(provider_data: list) -> float:
    """Получить сумму в EUR"""

    amount = 0

    for ticket in provider_data:
        total = float(ticket["pricing"]["total"])
        currency = ticket["pricing"]["currency"]
        amount += Currency.translate_currency(total, currency, "EUR")

    return amount


def get_provider_data(app_name: str, search_id: int):
    """Получить данные с провайдера"""

    provider_url = reverse("{0}:search".format(app_name))
    provider_data = requests.post(os.getenv('BASE_URL') + provider_url).json()

    search_result = SearchResult.objects.get(search_id=search_id)
    search_result.amount += get_amount(provider_data)
    search_result.items += provider_data
    search_result.save()


async def update_search_result(search_id: int):
    """Обновить результат поиска"""

    tasks = [asyncio.create_task(sync_to_async(get_provider_data)(app_name, search_id))
             for app_name in ("provider_a", "provider_b")]

    await asyncio.gather(*tasks)
