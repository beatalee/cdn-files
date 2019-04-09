# coding:utf-8

import sys, os

NginxBaseDir = "/etc/nginx"
#CorRuleSaveDir="/usr/local/share/owasp-modsecurity-crs"
DataInItalDir = "/home/modsecurity/inital_data"
SplitSigal = "/"

## window 下的配置只是为了方便本地调试接口方便
if sys.platform == "win32":
    NginxBaseDir = "E:\\nginx_conf"
    DataInItalDir = "F:\\workspace\\docs\\init_data\\data_inital"
    SplitSigal = "\\"


## Nginx设置和WAF引擎配置文件设置
NginxConfFile = os.path.join(NginxBaseDir, "nginx.conf")
NginxWAFConfFile = os.path.join(NginxBaseDir, "vhost", "waf.conf") ## 修改waf配置

## Web 扫描器
ScannersUADatasFile = os.path.join(NginxBaseDir, "rules", "scanners-user-agents.data")
ScriptUADatasFile = os.path.join(NginxBaseDir, "rules", "scripting-user-agents.data")

## 搜索引擎机器人
SerchEngineCrawlersUAFile = os.path.join(NginxBaseDir, "rules", "crawlers-user-agents.data")

## 状态码过滤文件
RestrictStatusCodeFile = os.path.join(NginxBaseDir, "prule", "restrict-status-files.data")

## 2019-4-9 增加referer
ValidRefererFile = os.path.join(NginxBaseDir, "patch_rules", "valid_referer.data")

import os
if not os.path.exists(ValidRefererFile):
    os.system("touch {}".format(ValidRefererFile))


