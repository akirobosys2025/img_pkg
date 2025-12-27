#!/bin/bash

dir=~
[ "$1" != "" ] && dir="$1"

cd $dir/ros2_ws
colcon build
source $dir/.bashrc
ros2 launch img_pkg exte_denoi.launch.py & LAUNCH_PID=$!

sleep 5

python3 - <<EOF
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np

rclpy.init()
node = Node('test_pub')
pub = node.create_publisher(Image, 'raw_img', 10)
bridge = CvBridge()

dummy_image = (np.random.rand(480, 640, 3) * 255).astype(np.uint8)
msg = bridge.cv2_to_imgmsg(dummy_image, 'bgr8')
pub.publish(msg)

rclpy.spin_once(node, timeout_sec=1.0)
node.destroy_node()
rclpy.shutdown()
EOF

OUTPUT=$(timeout 5 ros2 topic echo /denoised_img -n 1)
if [[ -z "$OUTPUT" ]]; then
  echo "Test failed: no denoised image received!"
  kill $LAUNCH_PID
  exit 1
else
  echo "Test passed: denoised image received."
fi

kill $LAUNCH_PID

