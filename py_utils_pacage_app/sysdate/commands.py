# coding:utf-8

# 修改系统时间 - `timedatectl set-ntp yes`
hk_dt_show = "hwclock --show"  ## 展示硬件时间

# modify_sys_date = "timedatectl set-time {date}"  ## 修改系统日期
# modify_sys_time = "timedatectl set-time {time}"  ## 修改系统时间
# run_systohc = "hwclock --systohc --localtime " ## 硬件时间随着系统时间修改

modify_sys_datetime = "timedatectl set-time {date} && timedatectl set-time {time} && hwclock --systohc --localtime "







