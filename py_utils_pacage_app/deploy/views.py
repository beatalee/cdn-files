from rest_framework import serializers, viewsets, routers

from .models import ProxySetting, LoadBalanceConfig, WebServerHost
from .serializers import ProxySettingSerializer, LoadBalanceConfigSerializer, WebServerHostSerializer
from .pagination import ShowAllPaginationLimit100


class ProxySettingViewSet(viewsets.ModelViewSet):
    queryset = ProxySetting.objects.all()
    serializer_class = ProxySettingSerializer
    pagination_class = ShowAllPaginationLimit100


class LoadBalanceConfigViewSet(viewsets.ModelViewSet):
    queryset = LoadBalanceConfig.objects.all()
    serializer_class = ShowAllPaginationLimit100


class WebServerHostViewSet(viewsets.ModelViewSet):
    queryset = WebServerHost.objects.all()
    serializer_class = WebServerHostSerializer
    pagination_class = ShowAllPaginationLimit100


# Routers provide a way of automatically determining the URL conf.
server_cfg_router = routers.DefaultRouter()
server_cfg_router.register(r'proxy_setting', ProxySettingViewSet)      ### URL的 Debug 测试
server_cfg_router.register(r'load_balance_cfg', LoadBalanceConfigViewSet)      ### URL下白名单IP
server_cfg_router.register(r'webserver_host', WebServerHostViewSet)      ### URL下白名单IP




