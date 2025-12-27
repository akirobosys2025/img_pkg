#!/bin/bash

dir=~
[ "$1" != "" ] && dir="$1"

cd $dir/ros2_ws
colcon build
source $dir/.bashrc 　
timeout 10 ros2 launch img_pkg exte_denoi.launch.py > /tmp/img_pkg.log

cat /tmp/img_pkg.log |
grep 'Listen: 10'
