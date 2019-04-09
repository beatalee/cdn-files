# coding:utf-8
from datetime import datetime
import pymongo

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

## 权限控制 2018-11-8
from wafmanage.permissions.plat_permissions import SecurityPermission

# Mongo存储当前的配置状态 #################
from phaser1.apscheduler.utils.mongo import MongoConn
from phaser1.apscheduler.config import WafMongoConfig

from .local_cfg import NginxConfCollectionName
# from .inintal_cfg import origin_cfg

def get_lattest_nginx_conf_cfg():
    ldc = WafMongoConfig.copy()
    ldc["db_name"] = 'waf'

    # from website.settings import PLAT_INITAL
    # if True:
    #     MongoConn(ldc).db[NginxConfCollectionName].remove()

    try:
        data = MongoConn(ldc).db[NginxConfCollectionName].find(projection={"_id": False}).sort([("add_dt", pymongo.DESCENDING), ])[0]
        return data["cfg"]
    except:
        return origin_cfg


def add_cfg_to_mongo(request, _instance):
    ldc = WafMongoConfig.copy()
    ldc["db_name"] = 'waf'
    from website.settings import PLAT_INITAL
    if PLAT_INITAL:
        MongoConn(ldc).db[NginxConfCollectionName].remove()
    _settings = {}
    _settings.setdefault("add_dt", datetime.now())
    _settings.setdefault("opreate_user", request.user.username)
    _settings.setdefault("cfg", _instance)
    MongoConn(ldc).db[NginxConfCollectionName].insert(_settings)

## 通知管理
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, SecurityPermission))
def set_nginx_conf_cfg(request):
    return common_nginx_conf(request)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, SecurityPermission))
def get_nginx_conf_cfg(request):

    return Response({"data": get_lattest_nginx_conf_cfg(), "stat": "获取成功"})


# from wafmanage.dprocess import get_command
from ..nginx_txt.utils import origin_cfg, NginxConf
def nginx_inital_conf(origin_cfg=origin_cfg):
    conf_header = NginxConf(cfg=origin_cfg).get_header()
    server_content = NginxConf(cfg=origin_cfg).get_server_content()
    return conf_header + "\n" + server_content


def common_nginx_conf(request):
    from ..file_config import NginxWAFConfFile
    data = request.GET if request.method == "GET" else request.data
    out_settings = get_lattest_nginx_conf_cfg().copy()

    # if "init" in data.keys():
    #     get_command("mv -f {nginx_conf} {nginx_conf}.bak").format(nginx_conf=NginxWAFConfFile)
    #     with open(NginxWAFConfFile, "w+", encoding="utf-8") as f:
    #         f.write(nginx_inital_conf() )
    #         f.close()
    #     return Response({"stat": "初始化成功", "reason": "初始化Nginx配置"})

    ## 默认未开启ssl
    if "ssl" in data.keys():
        out_settings["ssl"] = ""
        out_settings["no_ssl"] = "#"
    else:
        out_settings["ssl"] = "#"
        out_settings["no_ssl"] = ""

    ## 默认未开启防盗链
    if "fdl" in data.keys():
        out_settings["start_fdl"] = False

    ## 默认未开启 ddos
    if "cc" in data.keys():
        out_settings["limit_per_second"] = ""

    ## 默认模板种类选择为2
    if "tid" in data.keys():
        out_settings["tid"] = int(data["tid"])

    ## WAF 防护端口设置
    if "local_server_port" in data.keys():
        out_settings["local_server_port"] = int(data["local_server_port"])

    ## 默认模板种类选择为2
    if "server_name" in data.keys():
        out_settings["server_name"] = data["server_name"]

    try:
        return Response({"stat": "修改配置成功", "settings": out_settings})
    finally:
        add_cfg_to_mongo(request, out_settings)
        with open(NginxWAFConfFile, "w+", encoding="utf-8") as f:
            f.write(nginx_inital_conf(origin_cfg=out_settings))
            f.close()

## _data = json.loads(request.body.decode())
import json

@api_view(['POST'])
@permission_classes((IsAuthenticated, SecurityPermission) )
def mg_nginx_conf_location(request):
    from ..file_config import NginxWAFConfFile

    data = json.loads(request.body.decode())
    # print(data)
    # data["test22222"] = 23232
    # print(data)
    # print("=-=====")
    # data = request.data if request.method == "POST" else request.GET
    # res_pdata = dict(data) ## 修复form_data->json错误
    # res_pdata = {}
    # try:
    #     res_pdata["url_begin"] = data["url_begin"]
    # except:
    #     return Response({"reason": "url_begin参数传递错误"}, status=400)
    nginx_conf_cfg = get_lattest_nginx_conf_cfg().copy()
    _location_cfgs = nginx_conf_cfg["location_cfgs"]
    if "delete" in data.keys():
        if "url_begin" in data.keys():
            _del_urls = data["url_begin"].replace(" ","").split(",")
            for url_begin in [lcfg["url_begin"] for lcfg in _location_cfgs if "url_begin" in lcfg.keys()]:
                if url_begin in _del_urls:
                    item = [x for x in _location_cfgs if "url_begin" in x.keys() and  x["url_begin"] == url_begin]
                    for t in item:
                        _location_cfgs.remove(t)
        nginx_conf_cfg["location_cfgs"] = _location_cfgs
    elif "add" in data.keys():
        if "url_begin" not in data.keys():
            return Response({"reason": "参数传递错误"}, status=400)

        if "proxy" in data.keys():
            data["server_host"] = data["server_host"] if "server_host" in data.keys() else "$host:$server_port"
            data["cache_strategy"] = 1
            data["custom_error"] = 1
            data["proxy_cache"] = 1
        nginx_conf_cfg["location_cfgs"].append(data)

    try:
        return Response({"stat": "修改Nginx配置成功, 请稍后重启引擎使其生效", "params": data})
    finally:
        add_cfg_to_mongo(request, nginx_conf_cfg)
        with open(NginxWAFConfFile, "w+", encoding="utf-8") as f:
            f.write(nginx_inital_conf(origin_cfg=nginx_conf_cfg))
            f.close()