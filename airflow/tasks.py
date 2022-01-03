import asyncio
import json
import xmltodict
import requests

from celery import shared_task
from celery.signals import celeryd_after_setup

from .models import SearchResult
from .services import update_currency, update_search_result


@shared_task
def complete_search_result(search_id: int) -> None:
    """Обработать результат поиска"""

    asyncio.run(update_search_result(search_id))

    search_result = SearchResult.objects.get(search_id=search_id)
    search_result.status = "C"
    search_result.save()


@shared_task
@celeryd_after_setup.connect
def load_currencies(**kwargs) -> None:
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
