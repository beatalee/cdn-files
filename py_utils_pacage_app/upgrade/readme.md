# 升级模块

## 2018-11-28 

## 规则集升级
- 1, 升级核心规则文件
- 2, 升级自定义规则的补丁文件

## 升级管理平台
- 通过上传某个分支或者整个代码仓库进行升级
- 通过远程代码共享(SVN/GITLAB)实现升级


## Docker-Mysql 
```bash 
docker run --restart=always \
-p 3306:3306 \
--name=mysql -d \
-e 'DB_USER=admin105' \
-e 'DB_PASS=yesadmin@816' \
-e 'DB_NAME=phaser1' \
-e 'DB_REMOTE_ROOT_NAME=root' \
-e 'DB_REMOTE_ROOT_PASS=1q2w3e4R@ac' \
-e 'MYSQL_CHARSET=utf8mb4'  \
-e 'MYSQL_COLLATION=utf8_bin' \
-v /srv/docker/data/mysqldata:/var/lib/mysql \
sameersbn/mysql:5.7.22-1
```




