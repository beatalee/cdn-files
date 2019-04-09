# coding:utf-8
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from wafmanage.dprocess import get_command
from ..cfg import UpgradShellDir, FileUploadSaveDir,\
    NginxModsecRulePath, VERSION, PatchRulesPath
import os


upgrade_cfgs = {
    #"cor_rule": {"gaim_path": NginxModsecRulePath, "backup": True, "version": VERSION, "sync_shell": "\'nginx -s reload\'"},
    "patch_rule": {"gaim_path": PatchRulesPath, "backup": True, "version": VERSION, "sync_shell": "\'nginx -s reload\'"},
    #"plat_source": {"gaim_path": "/home/django/web", "backup": True, "version": VERSION, "sync_shell": "\'/bin/bash /home/django/replace.sh\'"},
}

@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated, ))
def upgrade_view(request):
    data = request.GET if request.GET else request.data
    saved_path_filename = data["filename"]
    saved_file_path = os.path.join(FileUploadSaveDir, saved_path_filename)
    replace_and_upgrade_shell = os.path.join(UpgradShellDir, "upgrade.sh")
    version = data["version"] if "version" in data.keys() else VERSION
    cfg_type = data["cfg_type"] if "cfg_type" in data.keys() else "patch_rule"

    _local_params = upgrade_cfgs[cfg_type]
    # params = [saved_file_path, _local_params["gaim_path"], version, 1, "echo ok"]
    params = [ saved_file_path, _local_params["gaim_path"], version, '1',  _local_params["sync_shell"]]
    current_shell_cmd = "/bin/bash {bin_file} {params}".format(
        bin_file=replace_and_upgrade_shell,
            params=" ".join(params) )
    responsed_stdout = get_command(current_shell_cmd)
    response = dict(current_shell_cmd=current_shell_cmd, responsed_stdout=responsed_stdout, )
    try:
        return Response(dict(response, stat=True))
    except:
        return Response(dict(response, stat=False), status=400)


