# coding:utf-8

import os
import sys
import django
########################### 本文件执不执行没区别 ##############################

def django_setup():
    DjangoModulePath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    sys.path.append(DjangoModulePath)
    os.chdir(DjangoModulePath)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
    django.setup()

import re
def cate():
    django_setup()
    from phaser1.models import RuleTxt2
    files = set([x.rule_belong_file for x in RuleTxt2.objects.all()])
    for file in files:
        # print(file)
        from phaser1.api.utils.regex import get_kv_of_rukes
        matched_d3_rule_key = re.match(".*?\-(\d+)\-.*?", file)
        if matched_d3_rule_key:
            matched_key_d3 = matched_d3_rule_key.group(1)
            if matched_key_d3 in get_kv_of_rukes().keys():
                print("========="+matched_key_d3+"=======")
                print(get_kv_of_rukes()[matched_key_d3])
                RuleTxt2.objects.filter(rule_belong_file=file).update(category=get_kv_of_rukes()[matched_key_d3])

            else:
                print(">>>>>>>>>>>>>>" + matched_key_d3)
                print(">>>>>>>>>>>>>>" + file)

if __name__ == '__main__':
    cate()
