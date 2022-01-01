from django.db import models


class Currency(models.Model):
    """Модель валюты"""

    fullname = models.CharField(max_length=128, verbose_name="Полное название")
    title = models.CharField(max_length=3, verbose_name="Название")
    description = models.FloatField(verbose_name="Сумма в KZT")

    @staticmethod
    def translate_currency(amount: float, from_currency_title: str, to_currency_title: str) -> float:
        """Перевести валюту к другой"""

        from_currency = Currency.objects.get(title=from_currency_title)
        to_currency = Currency.objects.get(title=to_currency_title)

        return amount * from_currency.description / to_currency.description

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"


class SearchResult(models.Model):
    """Модель результата поиска"""

    STATUSES = (
        ("P", "PENDING"),
        ("C", "COMPLETED"),
    )

    search_id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=1, choices=STATUSES, default="P", verbose_name="Статус")
    items = models.JSONField(null=True, default=list, verbose_name="Результат")
    amount = models.FloatField(default=0, verbose_name="Сумма в EUR")

    class Meta:
        verbose_name = "Результат поиска"
        verbose_name_plural = "Результаты поиска"
        ordering = ("amount", )
