#!/usr/bin/python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class NoiseFilterNode(Node):
    def __init__(self):
        super().__init__('denoi_img')

        self.bridge = CvBridge()

        self.sub = self.create_subscription(
            Image,
            'raw_img',
            self.image_callback,
            10
        )
        self.pub = self.create_publisher(
            Image,
            'denoised_img',
            10
        )

        self.get_logger().info('denoise image node started')

    def image_callback(self, msg):
        
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        denoised = cv2.GaussianBlur(cv_image, (5, 5), 0)
        
        #デバック用
        cv2.imshow('Denoise Image', denoised)
        cv2.waitKey(1) 

        out_msg = self.bridge.cv2_to_imgmsg(denoised, encoding='bgr8')
        out_msg.header = msg.header

        self.pub.publish(out_msg)


def main():
    rclpy.init()
    node = NoiseFilterNode()
    rclpy.spin(node)
    node.destroy_node()
    cv2.destroyAllWindows()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
