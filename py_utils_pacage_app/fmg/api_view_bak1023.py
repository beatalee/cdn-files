# coding:utf-8
import json
import re

from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response

# from django.forms.models import model_to_dict
from django.core.paginator import Paginator

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# from .permissions import IsAuditorOrAdmin
# from phaser1.models import RuleTxt2, RuleTag

from wafmanage.utils.db_utils import from_sql_get_data
# from .local_config import AccessLogPaginator, ModsecLogPaginator
from .file_config import NginxBaseDir, ScannersUADatasFile,\
    ScriptUADatasFile, SerchEngineCrawlersUAFile


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def web_scanner_file(requset):
    try:
        return test_file(requset, ScannersUADatasFile)
    except:
        return JsonResponse({"stat": "接口调用失败"}, status=403)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def serchengine_bot(requset):

    return test_file(requset, SerchEngineCrawlersUAFile)


############# 核心接口文件; 这里完全可以通过配置加载更多的远程文件编辑 #########
def test_file(request, File):
    # data = json.loads(request.body.decode())
    def get_scanner_datas():
        with open(File, "r+", encoding="utf-8") as f:
            lines = f.read().split("\n")
            f.close()

        res_datas = []
        for line in lines:
            false_matched = re.match("\#\s(.*)", line)
            true_matched = re.match("(.*)", line)
            if false_matched:
                res_datas.append((false_matched.group(1), False))
            elif true_matched:
                res_datas.append((true_matched.group(1), True))
            else:
                res_datas.append((None, False))
        return res_datas

    def resave_scanner_data(res_datas):
        with open(File, "w+", encoding="utf-8") as f:
            f.write("\n".join([ str("# "+x[0]) if x[1]==False else str(x[0]) for x in res_datas ]) )
            f.close()

    if request.method == "GET":
        res_datas = get_scanner_datas()

        action_type = request.GET["type"] if "type" in request.GET.keys() else None
        if action_type:
            res_datas = get_scanner_datas()
            ## 增加元素
            if action_type == "add":
                res_datas.append( (request.GET["scanner"], True) )
            # stats = [res_datas.remove(x) for x in res_datas if x[0]["scanner"] == request.GET["scanner"] ]
            ## 初始化文件对象
            if action_type == "inital":
                from wafmanage.dprocess import get_command
                get_command("rm -f {path} && mv {path}.bak {path}".format(path=ScriptUADatasFile) )

                return JsonResponse({"stat": True, "reason": "复位成功"})

            ## 在列表中删除这个元素
            if action_type == "delete":
                if "scanner" in request.GET.keys():
                    [res_datas.remove(x) for x in res_datas if x[0] == request.GET["scanner"]]

            ## 修改为真和假
            if action_type == "update":
                gaim_stat = True if "retrue" in request.GET.keys() else False
                _new_datas = []
                if "scanner" in request.GET.keys():
                    for x in res_datas:
                        if x[0] != request.GET["scanner"]:
                            _new_datas.append(x)
                        else:
                            _new_datas.append( (x[0], gaim_stat) )
                res_datas = _new_datas

            if action_type == "download":
                return JsonResponse({"reson": "此处不提供下载;下载规则模板即可查看"})

        try:
            return JsonResponse({"datas": [x for x in res_datas if x[0] != ""]})
        finally:
            resave_scanner_data(res_datas)


        ## 教程
        # 展示所有的 ScannerUA 客户端 http://localhost:3322/waf/p1/test_file
        # 增加一个 ScannerUA http://localhost:3322/waf/p1/test_file?type=add&scanner=CCTV
        # 修改一个 ScannerUA http://localhost:3322/waf/p1/test_file?type=update&scanner=CCTV&&retrue=223
        # 删除一个 ScannerUA http://localhost:3322/waf/p1/test_file?type=delete&scanner=CCTV

from wafmanage.dprocess import get_command
from .nginx_txt.utils import origin_cfg, NginxConf
def nginx_inital_conf(origin_cfg=origin_cfg):
    conf_header = NginxConf(cfg=origin_cfg).get_header()
    server_content = NginxConf(cfg=origin_cfg).get_server_content()
    return conf_header + "\n" + server_content


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def modify_nginx_conf(request):
    from .file_config import NginxWAFConfFile
    data = request.GET if request.method == "GET" else request.data
    out_settings = origin_cfg.copy()

    if "init" in data.keys():
        get_command("mv -f {nginx_conf} {nginx_conf}.bak").format(nginx_conf=NginxWAFConfFile)
        with open(NginxWAFConfFile, "w+", encoding="utf-8") as f:
            f.write(nginx_inital_conf() )
            f.close()
        return Response({"stat":"初始化成功", "reason": "初始化Nginx配置"})

    ## 默认未开启ssl
    if "ssl" in data.keys():
        out_settings["ssl"] = ""
        out_settings["no_ssl"] = "#"

    ## 默认未开启ssl
    if "no_ssl" in data.keys():
        out_settings["ssl"] = "#"
        out_settings["no_ssl"] = ""

    ## 默认未开启防盗链
    if "fdl" in data.keys():
        out_settings["start_fdl"] = False

    ## 默认未开启 ddos
    if "ddos" in data.keys():
        out_settings["limit_per_second"] = True

    ## 默认模板种类选择为2
    if "tid" in data.keys():
        out_settings["tid"] = int(data["tid"])

    ## WAF 防护端口设置
    if "local_server_port" in data.keys():
        out_settings["local_server_port"] = int(data["local_server_port"])

    ## 路径指向配置; 需严格安装 config 规定来
    if "locations" in data.keys() and request.method == "POST":
        for x in data["locations"]:
            out_settings["location_cfgs"].append(x)

    try:
        return Response({"stat": "修改Nginx配置成功, 请稍后重启引擎使其生效", "params": data})
    finally:
        with open(NginxWAFConfFile, "w+", encoding="utf-8") as f:
            f.write(nginx_inital_conf(origin_cfg=out_settings))
            f.close()