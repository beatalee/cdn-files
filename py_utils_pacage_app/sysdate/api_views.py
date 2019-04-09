# coding:utf-8

import os
from rest_framework.response import Response
from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
# from .permissions import IsAuditorOrAdmin
# from wafmanage.permissions.plat_permissions import SecurityPermission

from .commands import hk_dt_show, modify_sys_datetime
from wafmanage.dprocess import get_command
from wafmanage.utils.db_utils import from_sql_get_data

@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated, ))
def update_hw_dt(request):
    ## {"systime":"2018-11-12 16:25:33"}
    if request.method == 'POST':
        str_dt = request.data["systime"]
        stats_str = []

        import re
        datas_matched = re.match("(.*?)\s(.*)", str_dt)
        if datas_matched:
            date = datas_matched.group(1)
            time = datas_matched.group(2)
            get_command(modify_sys_datetime.format(date=date, time=time))
            stats_str.append({"update_dt": date + " " + time})
        else:
            return Response({"reson":"验证传入参数是否是 YYYY-MM-DD HHmmss 格式"})

        return Response({"stat":"修改成功", "datas": stats_str})

    if request.method == 'GET':
        return Response({"hw": get_command(hk_dt_show)})

from django.views.decorators.cache import cache_page
@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
@cache_page(1*3600)
def index_view_cates(request):
    query_sql = """select category, count(category) as ccate from (select category from 
	(select tt4.*, modsechinfo.matched_data from 
	(select rulecate.category, t4.* from 
	 (select audit_logid, any_value(cate_id) as cate_id, max(ccate) as mc, any_value(hid) as hid, any_value(cn_msg) as cn_msg, any_value(rule_id) as m_rid from 
	  (select audit_logid, count(cate_id) as ccate, cate_id, any_value(hid) as hid, any_value(cn_msg) as cn_msg, any_value(rule_id) as rule_id from 
		(select c.*,ruletxt.cn_msg, if(isnull(ruletxt.cate_id), 404, ruletxt.cate_id) as cate_id from 
			  (select a11.*, modsechinfo.matched_data,modsechinfo.rule_id from 
				(select a1.*, b1.modseclogphaserhinfo_id as hid  from 
					(select * from modseclog where id >0 order by audit_time desc ) as a1
					 left join modseclog_hloginfo as b1
					on a1.id = b1.modseclogdetail_id) as a11 
					left join 
					modsechinfo
					on modsechinfo.id = a11.hid) as c 
					left join ruletxt
					on ruletxt.rule_id=c.rule_id) as main_t group by audit_logid, cate_id  )  as t2
				   group by audit_logid ) as t4 left join rulecate on rulecate.id=t4.cate_id) as tt4
					left join modsechinfo on modsechinfo.id = tt4.hid ) as t5
					 left join modseclog on modseclog.audit_logid=t5.audit_logid 
					 ) as t_cate 
					 group by category order by ccate desc;"""
    return Response({"datas": from_sql_get_data(query_sql)["data"]})


