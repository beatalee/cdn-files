# coding:utf-8
import json
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import ProxySetting, WebServerHost

@api_view(['GET'])
def get_serverhost(request):
    return Response(WebServerHost.objects.get(id=int(request.GET["id"])))


