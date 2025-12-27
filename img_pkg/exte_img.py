#!/usr/bin/python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os

class FileImagePublisher(Node):
    def __init__(self):
        super().__init__('exte_img')

        self.declare_parameter('image_path', '')
        self.declare_parameter('fps', 5)
        self.declare_parameter('width', 640)
        self.declare_parameter('height', 480)

        self.image_path = self.get_parameter('image_path').get_parameter_value().string_value
        self.fps = self.get_parameter('fps').value
        self.width = self.get_parameter('width').value
        self.height = self.get_parameter('height').value

        if not self.image_path or not os.path.isfile(self.image_path):
            self.get_logger().error(f'Invalid image_path: {self.image_path}')
            raise RuntimeError('Invalid image_dir')


        self.bridge = CvBridge()
        self.pub = self.create_publisher(Image, 'raw_img', 10)
        self.timer = self.create_timer(1.0 / self.fps, self.timer_callback)

        self.get_logger().info(f'Publishing image: {self.image_path} at {self.fps} Hz')

    def timer_callback(self):
        image = cv2.imread(self.image_path)
        if image is None:
            self.get_logger().warn(f'Failed to read {self.image_path}')
            return

        image = cv2.resize(image, (self.width, self.height))
        msg = self.bridge.cv2_to_imgmsg(image, encoding='bgr8')
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'file_camera'

        self.pub.publish(msg)

def main():
    rclpy.init()
    node = FileImagePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

