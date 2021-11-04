import os
import json
from django.conf import settings
from django.test import TestCase
from .models import Currency
from .services import load_currencies, update_currency, get_amount


class AirflowTest(TestCase):
    """Тесты для Airflow"""

    def setUp(self):
        load_currencies()

    def test_translate_currency_kzt_to_kzt(self):
        amount = 2349821
        self.assertEquals(amount, Currency.translate_currency(amount, "KZT", "KZT"))

    def test_translate_currency_kzt_to_eur(self):
        amount = 1203012
        eur = Currency.objects.get(title="EUR")
        self.assertEquals(amount / eur.description, Currency.translate_currency(amount, "KZT", "EUR"))

    def test_translate_currency_eur_to_kzt(self):
        amount = 7123215
        eur = Currency.objects.get(title="EUR")
        self.assertEquals(amount * eur.description, Currency.translate_currency(amount, "EUR", "KZT"))

    def test_translate_currency_eur_to_eur(self):
        amount = 1231241
        self.assertEquals(amount, Currency.translate_currency(amount, "EUR", "EUR"))

    def test_translate_currency_rub_to_usd(self):
        amount = 1231231
        rub = Currency.objects.get(title="RUB")
        usd = Currency.objects.get(title="USD")

        self.assertEquals(
            amount * rub.description / usd.description,
            Currency.translate_currency(amount, "RUB", "USD")
        )

    def test_update_currency_update(self):
        update_currency({
            "fullname": "РОССИЙСКИЙ РУБЛЬ",
            "title": "RUB",
            "description": "456",
        })
        rub = Currency.objects.get(title="RUB")

        self.assertEquals(456, rub.description)

    def test_update_currency_create(self):
        update_currency({
            "fullname": "ВАЛЮТА",
            "title": "NNN",
            "description": "101",
        })

        try:
            Currency.objects.get(title="NNN")
            self.assertTrue(True)
        except Currency.DoesNotExist:
            self.assertTrue(False)

    def test_get_amount_response_a(self):
        file_location = os.path.join(settings.STATIC_ROOT, "response_a.json")
        file = open(file_location, "r")
        response_a = json.loads(file.read())
        file.close()
        self.assertEquals(114526.67000000017, get_amount(response_a))

    def test_get_amount_response_b(self):
        file_location = os.path.join(settings.STATIC_ROOT, "response_b.json")
        file = open(file_location, "r")
        response_a = json.loads(file.read())
        file.close()
        self.assertEquals(542.4879588780508, get_amount(response_a))

