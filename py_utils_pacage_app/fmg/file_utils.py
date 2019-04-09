# coding:utf-8

import re
import os
from rest_framework.response import Response
from .file_config import SplitSigal, DataInItalDir


def test_file(request, File, CAT=True):
    def get_scanner_datas():
        from wafmanage.dprocess import get_command
        lines = get_command("cat {}".format(File)).split("\r\n")
        res_datas = []
        for line in lines:
            false_matched = re.match("\#\s(.*)", line)
            true_matched = re.match("(^[0-9a-zA-z].*)", line)
            if false_matched:
                res_datas.append((false_matched.group(1), False))
            elif true_matched:
                res_datas.append((true_matched.group(1), True))
            else:
                res_datas.append((None, False))
        return res_datas

    def resave_scanner_data(res_datas):
        from wafmanage.dprocess import get_command
        res_str_eof = "&&&".join(["# "+ str(x[0]) if x[1]==False else str(x[0]) for x in res_datas ])
        # get_command("cat > {file} <<-EOF\n{str}\nEOF ".format(file=File, str=res_str_eof))
        # resave_command = "cat > {file} <<-EOF\n{str}".format(file=File, str=res_str_eof)
        resave_command = "echo '{str}' | sed 's/&&&//\/\n/g' > {file}".format(file=File, str=res_str_eof)
        get_command(resave_command)

        import logging
        logger = logging.getLogger('collect')
        logger.info("复位文件记录命令进行测试")
        logger.warn(resave_command)

    res_datas = get_scanner_datas()

    request_data = request.GET if request.method == "GET" else request.data
    action_type = request_data["type"] if "type" in request_data.keys() else None
    if action_type:
        # res_datas = get_scanner_datas()
        ## 增加元素
        if action_type == "add":
            res_datas.append( (request_data["scanner"], True) )
        # stats = [res_datas.remove(x) for x in res_datas if x[0]["scanner"] == request.GET["scanner"] ]
        ## 初始化文件对象
        if action_type == "inital":
            from wafmanage.dprocess import get_command
            # get_command("rm -f {path} && mv {path}.bak {path}".format(path=File) )
            inintal_file = os.path.join(DataInItalDir, str(File).split(SplitSigal)[-1] )
            get_command("rm -f {path} && cp {inintal_file} {path}".format(path=File, inintal_file=inintal_file) )

            return Response({"stat": True, "reason": "复位成功"})

        ## 在列表中删除这个元素
        if action_type == "delete":
            if "scanner" in request_data.keys():
                [res_datas.remove(x) for x in res_datas if x[0] == request_data["scanner"]]

        ## 修改为真和假
        if action_type == "update":
            gaim_stat = True if "retrue" in request_data.keys() else False
            _new_datas = []
            if "scanner" in request_data.keys():
                for x in res_datas:
                    if x[0] != request_data["scanner"]:
                        _new_datas.append(x)
                    else:
                        _new_datas.append((x[0], gaim_stat) )
            res_datas = _new_datas

        if action_type == "download":
            return Response({"reason": "此处不提供下载;下载规则模板即可查看"})

    try:
        return Response({"datas": [x for x in res_datas if x[0] != ""], "request_data": request_data})
    finally:
        resave_scanner_data(res_datas)

        ## 教程
        # 展示所有的 ScannerUA 客户端 http://localhost:3322/waf/p1/test_file
        # 增加一个 ScannerUA http://localhost:3322/waf/p1/test_file?type=add&scanner=CCTV
        # 修改一个 ScannerUA http://localhost:3322/waf/p1/test_file?type=update&scanner=CCTV&&retrue=223
        # 删除一个 ScannerUA http://localhost:3322/waf/p1/test_file?type=delete&scanner=CCTV

############# 核心接口文件; 这里完全可以通过配置加载更多的远程文件编辑 #########
def old_test_file(request, File):
    # data = json.loads(request.body.decode())
    def get_scanner_datas():
        with open(File, "r+", encoding="utf-8") as f:
            lines = f.read().split("\n")
            f.close()

        res_datas = []
        for line in lines:
            false_matched = re.match("\#\s(.*)", line)
            true_matched = re.match("(^[0-9a-zA-z].*)", line)
            if false_matched:
                res_datas.append((false_matched.group(1), False))
            elif true_matched:
                res_datas.append((true_matched.group(1), True))
            else:
                res_datas.append((None, False))
        return res_datas

    def resave_scanner_data(res_datas):
        with open(File, "w+", encoding="utf-8") as f:
            f.write("\n".join([ "# "+ str(x[0])  if x[1]==False else str(x[0]) for x in res_datas ]) )
            f.close()
    res_datas = get_scanner_datas()

    request_data = request.GET if request.method == "GET" else request.data
    action_type = request_data["type"] if "type" in request_data.keys() else None
    if action_type:
        res_datas = get_scanner_datas()
        ## 增加元素
        if action_type == "add":
            res_datas.append( (request_data["scanner"], True) )
        # stats = [res_datas.remove(x) for x in res_datas if x[0]["scanner"] == request.GET["scanner"] ]
        ## 初始化文件对象
        if action_type == "inital":
            from wafmanage.dprocess import get_command
            # get_command("rm -f {path} && mv {path}.bak {path}".format(path=File) )
            inintal_file = os.path.join(DataInItalDir, str(File).split(SplitSigal)[-1] )
            get_command("rm -f {path} && cp {inintal_file} {path}".format(path=File, inintal_file=inintal_file) )

            return Response({"stat": True, "reason": "复位成功"})

        ## 在列表中删除这个元素
        if action_type == "delete":
            if "scanner" in request_data.keys():
                [res_datas.remove(x) for x in res_datas if x[0] == request_data["scanner"]]

        ## 修改为真和假
        if action_type == "update":
            gaim_stat = True if "retrue" in request_data.keys() else False
            _new_datas = []
            if "scanner" in request_data.keys():
                for x in res_datas:
                    if x[0] != request_data["scanner"]:
                        _new_datas.append(x)
                    else:
                        _new_datas.append( (x[0], gaim_stat) )
            res_datas = _new_datas

        if action_type == "download":
            return Response({"reason": "此处不提供下载;下载规则模板即可查看"})

    try:
        return Response({"datas": [x for x in res_datas if x[0] != ""]})
    finally:
        resave_scanner_data(res_datas)

    ## 教程
    # 展示所有的 ScannerUA 客户端 http://localhost:3322/waf/p1/test_file
    # 增加一个 ScannerUA http://localhost:3322/waf/p1/test_file?type=add&scanner=CCTV
    # 修改一个 ScannerUA http://localhost:3322/waf/p1/test_file?type=update&scanner=CCTV&&retrue=223
    # 删除一个 ScannerUA http://localhost:3322/waf/p1/test_file?type=delete&scanner=CCTV

