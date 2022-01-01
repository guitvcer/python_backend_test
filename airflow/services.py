from .models import Currency
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
