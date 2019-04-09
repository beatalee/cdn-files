# coding:utf-8

import os, sys
from website.settings import MEDIA_DIR

NginxModsecRulePath = "/etc/nginx/rules"
ErrorPagesPathPartern = "/home/error_templates/htmls/{template_id}" ## 传递进去模板ID
AccessLogDir = "/home/logs/nginx"
ErrorPagesPath = "/home/error_templates/htmls"

FileUploadSaveDir = os.path.join(MEDIA_DIR, "uploads")
UpgradShellDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shells")
PatchRulesPath= "/etc/nginx/patch_rules" ##介于自定义规则和内置规则之间的补丁规则
VERSION="v0.1.11.28-beta"

WebPlatSource="/home/django/web"

## window 下的配置只是为了方便本地调试接口方便
if sys.platform == "win32":
    NginxModsecRulePath = "F:\\workspace\\waf-phaser1\\owasp-modsecurity-crs-3.0-master\\rules\\"
    ErrorPagesPathPartern = "F:\\BaiduNetdiskDownload\\ErrorPages-master\\ErrorPages-master\\error_page{template_id}"
    AccessLogDir="E:\\nginx"
    PatchRulesPath=os.path.join(AccessLogDir, "patch_rules")
    WebPlatSource="E:\\web"

for _dir in [FileUploadSaveDir, PatchRulesPath]:
    if not os.path.exists(_dir):
        os.makedirs(_dir)