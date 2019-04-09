from django.conf.urls import url, include

from .util_views import get_nginx_conf_cfg, set_nginx_conf_cfg, mg_nginx_conf_location

nginxconf_urlparterns = [
    url("^nginx_conf", get_nginx_conf_cfg),
    url("^mg_location", mg_nginx_conf_location),
    url("^set_c_nginx_conf_cfg", set_nginx_conf_cfg),
]
