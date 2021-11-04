from rest_framework import serializers
from .models import Currency, SearchResult


class CurrencySerializer(serializers.ModelSerializer):
    """Serializer модели валюты"""

    def save(self, **kwargs):
        try:
            currency = Currency.objects.get(fullname=self.validated_data["fullname"])
            currency.description = self.validated_data["description"]
            currency.save()
        except Currency.DoesNotExist:
            super().save(**kwargs)

    class Meta:
        model = Currency
        fields = ('fullname', 'title', 'description')


class SearchResultIdSerializer(serializers.ModelSerializer):
    """Serializer id результата поиска"""

    class Meta:
        model = SearchResult
        fields = ('search_id', )


class SearchResultSerializer(serializers.ModelSerializer):
    """Serializer модели результата поиска"""

    status = serializers.CharField(source="get_status_display")
    price = serializers.SerializerMethodField("get_price")

    def get_price(self, instance: SearchResult) -> dict:
        currency_title = self.context["currency"]
        amount = Currency.translate_currency(instance.amount, "EUR", currency_title)

        return {
            "amount": str(int(amount * 100) / 100),
            "currency": currency_title,
        }

    class Meta:
        model = SearchResult
        fields = ('search_id', 'status', 'items', 'price')
