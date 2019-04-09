# coding:utf-8

origin_cfg = dict(
    limit_per_second="#",
    modsec="",
    ssl="#",
    no_ssl="",
    tid=0,
    modsec_conf_path="/etc/nginx/modsecurity.conf",
    local_server_port=80,
    server_name="waf.kac.fun kac.fun",
    ## 防盗链
    start_fdl=False,

    location_cfgs = [
        {"url_begin":"/",
         "proxy":1,
         "proxy_cache": 1,
         "server_host":"$host:$server_port",
         "proxy_server":"http://192.168.2.110:9070",
         "cache_strategy": 1,
         "custom_error": 1,
         },
        # {"url_begin": "/WebGoat", "proxy": 1,
        #  "server_host": "192.168.3.2:1180",
        #  "proxy_server": "http://192.168.2.9:7080/WebGoat",
        #   "custom_error": 1, },
        # {"url_begin":"/test403", "return_code": 403},
        # {"url_begin":"/test503", "return_code": 503},
        # {"url_begin":"/test513", "return_code": 413},
        {"url_begin":"/test_waf", "return_code": 200},
        {"url_begin":"/site_demo", "static":1, "site_path": "/home/django/web/phaser1/"},
        {"url_begin":"/uploads", "file_show_save_path": "/home/files/uploads"},
        {"url_begin":"/error_pages", "alias": "/home/error_templates/htmls"},
    ]

)


location_proxy = """
{proxy_cache}
proxy_pass {proxy_server};
proxy_redirect off;
proxy_set_header Host {server_host};
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
client_max_body_size 10m;
client_body_buffer_size 128k;
proxy_connect_timeout 90;
proxy_send_timeout 90;
proxy_read_timeout 90;
proxy_buffer_size 64k;
proxy_buffers 32 32k;
proxy_busy_buffers_size 128k;
proxy_temp_file_write_size 128k;

proxy_cache_key $proxy_host$request_uri$cookie_jessionid;
{cache_cn}proxy_cache_valid 200 302 10m;    #为响应码是200和302的资源，设置缓存时长为10分钟
{cache_cn}proxy_cache_valid 404      1m;    #为响应码是404的资源，设置的缓存的时长为1分钟
{cache_cn}proxy_cache_valid 500 502  0m;

{custom_error}
"""

conf_header = """limit_req_zone $binary_remote_addr zone=allips:10m rate=20r/s;
proxy_cache_path /tmp/ levels=1:2 keys_zone=cya_waf_cache:10m max_size=10g inactive=60m use_temp_path=off;

log_format  custom '$remote_addr - $remote_user [$time_local] '
'"$request" $status $body_bytes_sent '
'"$http_referer" "$http_user_agent" '
'"$http_x_forwarded_for" $request_id ';

# fastcgi_intercept_errors on;"""

fileshow="""
root {file_show_save_path};
autoindex on;  # 开启目录文件列表
autoindex_exact_size on;  # 显示出文件的确切大小，单位是bytes
autoindex_localtime on;  # 显示的文件时间为文件的服务器时间
charset utf-8,gbk;  # 避免中文乱码
"""

server_content_head = """{modsec}modsecurity on;
{modsec}modsecurity_rules_file {modsec_conf_path};

{no_ssl}listen       {local_server_port};
{ssl}listen       {local_server_port} ssl;
server_name  {server_name};

{ssl}ssl_certificate /etc/nginx/ssl/nginx-selfsigned.crt;
{ssl}ssl_certificate_key /etc/nginx/ssl/nginx-selfsigned.key;

access_log  /var/log/nginx/waf.access.log custom;

{limit_per_second}limit_req zone=allips burst=5 nodelay;

"""

fdl_partern = """
location ~* \.(gif|jpg|png|jpeg|js|css)$ $%^
    expires     30d;
    valid_referers none blocked {server_name};
    if ($invalid_referer) $%^
      rewrite ^/ /fangdaolian;
    ^%$
^%$
"""