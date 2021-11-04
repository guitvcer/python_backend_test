from django.urls import path
from .views import SearchView


app_name = "provider_a"

urlpatterns = [
    path('search', SearchView.as_view(), name="search")
]
