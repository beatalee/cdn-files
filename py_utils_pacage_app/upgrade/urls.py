from django.conf.urls import url, include

from .ajax_upload import ajax_upload, upload_cor_rules, upload_hock_rules, upload_plat_source

ajax_upload_urlparterns = [
    url(r'^ajax_upload$', ajax_upload),

    # url(r'^upload_hock_rules$', upload_hock_rules),
    # url(r'^upload_cor_rules$', upload_cor_rules),
    # url(r'^upload_plat_source$', upload_plat_source),
]

## 2019-4-8 注释上面的接口。简化逻辑。

from .rule_upgrade.upgrade_views import upgrade_view
ajax_upload_urlparterns += [url(r'^upgrade$', upgrade_view),]
