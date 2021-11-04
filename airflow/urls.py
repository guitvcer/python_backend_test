from django.urls import path
from . import views


app_name = "airflow"

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('search', views.SearchView.as_view(), name="search"),
    path('results/<int:search_id>/<str:currency>', views.SearchResultView.as_view(), name="search_result"),
]
