#!/bin/bash

set -i

function upgrade(){
    cd /tmp;

    have_saved_filepath=$1 ## 上传文件的文件的绝对路径
    replaced_abs_path=$2 ## 需要替换的目标目录的目标的绝对路径

    replaced_gaim_dirdir=$(dirname ${replaced_abs_path}) ## 目标文件目录的上层目录
    replaced_gaim_dirname=${replaced_abs_path##*/} ## 目标目录的目标名

    version=$3   ## 手动输入的版本号的版本文件
    backup=$4
    async_shell=$5 ## 最后执行的处理脚本

    temp_path="/tmp/share"

    if [ ! -d "$temp_path" ] ; then
       mkdir -p $temp_path
    fi

    unzip $have_saved_filepath -d /tmp/share
    if [ ! -d "$temp_path$replaced_gaim_dirname" ]; then
        echo "压缩包文件不规范"
        echo "应该将["$replaced_gaim_dirname"]文件变成一个zip文件再进行上传"
        rm -rf $temp_path
        exit 0
    else
        rm -rf $temp_path ## 删除测试的中间文件
    fi

    if [ "$backup"  == "1" ]; then
        backed_up_path=$replaced_gaim_dirname".zip-"$(date -d "today" +"%Y%m%d%H%M%S") ;
        echo "进行中间备份到-->"$backed_up_path

        if [ ! -d "$replaced_abs_path" ]; then
            echo "待上传的目录是空目录"
        else
             echo "准备备份和转移"
             # cd $(dirname ${replaced_abs_path}) && \
             zip -q $backed_up_path $replaced_abs_path &&  mv $backed_up_path  /tmp/ ;
        fi
    fi
    echo "准备删除并解压文件到 -> "$replaced_gaim_dirdir
    rm -rf $replaced_abs_path &&  unzip $have_saved_filepath -d $replaced_gaim_dirdir \
    && echo $version > $replaced_abs_path/VERSION
    echo "已经完成了文件夹的替换"
    if [ "async_shell"  == "" ]; then
        echo "没有后续处理脚本"
    else
      $async_shell ;
    fi

}

## 测试: 把 root.zip 里面的所有内容 压缩到 /opt/test/ 下
#upgrade /home/flaskbb/root.zip /opt/root 0.3.2 1 'echo ok'
#upgrade /home/flaskbb/root.zip /opt/test 0.3.2 1 'echo ok'
upgrade $1 $2 $3 $4 $5