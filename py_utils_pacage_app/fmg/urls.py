from django.conf.urls import url, include

from .api_view import  web_scanner_file, serchengine_bot,\
    restrict_status_file, scripting_ua, valid_referer

fmg_urlparterns = [
    ## 扫描器
    url(r'^web_scanner_file',  web_scanner_file),

    ## 搜索引擎机器人客户端
    url(r'^serchengine_bot',  serchengine_bot),

    ## 爬虫脚本客户端
    url(r'^scripting_ua',  scripting_ua),

    ## 状态码过滤问题
    url(r'^restrict_status_file',  restrict_status_file),

    ## Valid_refer_file管理
    url(r'^valid_referer_file',  valid_referer),

]


from .nginx_txt.nginx_tool_urls import nginxconf_urlparterns
fmg_urlparterns.extend(nginxconf_urlparterns)

