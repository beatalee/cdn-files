# coding:utf-8
import json
import re
import os

from django.http import JsonResponse, HttpResponse

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# from .local_config import AccessLogPaginator, ModsecLogPaginator
from .file_config import NginxBaseDir, ScannersUADatasFile, SplitSigal,\
    ScriptUADatasFile, SerchEngineCrawlersUAFile, RestrictStatusCodeFile,\
    DataInItalDir, ValidRefererFile

# from wafmanage.permissions.plat_permissions import SecurityPermission
# from .file_utils import old_test_file as test_file
## 2019-3-9 替换原来的这个接口内容为当前这个枷锁的。
from phaser2.filemg_utils import old_test_file as test_file
## 2018-11-23 修复, 旨在解决跨机部署中open无效的问题
#from .file_utils import test_file

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def web_scanner_file(request):
    try:
        return test_file(request, ScannersUADatasFile, key_name='item')
    except:
        return JsonResponse({"stat": "扫描器接口调用失败"}, status=403)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def serchengine_bot(request):
    try:
        return test_file(request, SerchEngineCrawlersUAFile, key_name='item')
    except:
        return JsonResponse({"stat": "搜索引擎接口调用失败"}, status=403)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def scripting_ua(request):
    return test_file(request, ScriptUADatasFile, key_name='item')
    # try:
    #     return test_file(request, ScriptUADatasFile)
    # except:
    #     return JsonResponse({"stat": "接口调用失败"}, status=403)

#################### 状态吗过滤函数 #####################
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def restrict_status_file(request):
    try:
        return test_file(request, RestrictStatusCodeFile, key_name='item')
    except:
        return JsonResponse({"stat": "接口调用失败"}, status=403)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def valid_referer(request):
    # from phaser2.filemg_utils import old_test_file as t2file
    # return t2file(request, ValidRefererFile)
    try:
        return test_file(request, ValidRefererFile, key_name='item')
    except:
        return JsonResponse({"stat": "Referer管理接口调用失败"}, status=403)