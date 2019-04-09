from django.conf.urls import url, include

from .views import server_cfg_router

urlpatterns_server_cfg = [
    url(r'^server_cfg/', include(server_cfg_router.urls)),
]

from .api_view import get_serverhost

urlpatterns_server_cfg += [ url(r'^server_host$', get_serverhost ), ]