# coding:utf-8

import os, re

from django.http import HttpResponse, JsonResponse
from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .cfg import FileUploadSaveDir
from .file_utils import get_file_info_by_filepath


def ajax_upload(request, file_prefix_name="rule"):
    # 记录用户操作的行为历史
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        dt_str = str(datetime.now().date()).replace("-","_")
        # file_path_in_server = os.path.join(MEDIA_DIR, 'uploads', *dt_list, file_obj.name)
        file_path_in_server = os.path.join(FileUploadSaveDir, file_prefix_name + "_" + dt_str+ "_" + file_obj.name )
        f = open(file_path_in_server, 'wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        return HttpResponse("上传成功")

    if request.method == "GET":
        # 获取已经上传的那个目录下已经存在的文件, 列表
        files = os.listdir(FileUploadSaveDir)
        files.sort()
        # file_prefix = request.GET["prefix"]
        file_prefix = file_prefix_name
        gaim_saved_lists = []
        if len(files) > 0:
            for filename in files:
                matched = re.match("^" + file_prefix + "_\d+_\d+_\d+.*?", filename)
                if matched:
                    file_info = get_file_info_by_filepath(os.path.join(FileUploadSaveDir, filename))
                    gaim_saved_lists.append(dict(filename=filename, **file_info))

        return JsonResponse(dict(
            file_dir=FileUploadSaveDir,
            file_lists=gaim_saved_lists,
            file_prefix=file_prefix,
        ))


# 上传核心规则
@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated, ))
def upload_cor_rules(request):
    return ajax_upload(request=request, file_prefix_name="cor_rule")


# 上传补丁文件
@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated, ))
def upload_hock_rules(request):
    return ajax_upload(request=request, file_prefix_name="patch_rule")


# 上传项目源代码
@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated, ))
def upload_plat_source(request):
    return ajax_upload(request=request, file_prefix_name="plat_source")


