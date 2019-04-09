from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from .models import ProxySetting, WebServerHost, LoadBalanceConfig
from .utils import get_random_port

class ProxySettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProxySetting
        fields = ('location_rx', 'load_balance_name', 'proxy_pass', 'proxy_host', 'proxy_cache', 'id')


## WebServerHost 的过滤器
class WebServerHostSerializer(serializers.ModelSerializer):
    # proxyids = serializers.CharField(label=u'代理设置的ID集合', default="")

    class Meta:
        model = WebServerHost
        fields = ('id','servername', 'server_port', 'tid', 'ssl', 'modsecurity', 'antiTheft_chain', 'proxy_settings', 'config_name', 'server_desc')

## 对应的IP黑名单
class LoadBalanceConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadBalanceConfig
        fields = ('proxy_server', 'proxy_stat', 'upstream_name', 'id')
