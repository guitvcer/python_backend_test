import os
from django.conf import settings
from django.http import FileResponse
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from time import sleep


class SearchView(APIView):
    """Возвращает данные из response_a.json"""

    @staticmethod
    def post(*args, **kwargs):
        sleep(30)
        file_location = os.path.join(settings.STATIC_ROOT, "response_a.json")
        return FileResponse(open(file_location, "rb"), status=HTTP_200_OK)
