#!/usr/bin/env python3

"""
ROS2 IMAGE SUBSCIRBER NODE

This node subscribes to the '/image' topic and display image.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')

        # Subscriber to read raw image
        self.subscription_ = self.create_subscription(
            Image,
            '/image',
            self.callback_image,
            10
        )

        self.bridge = CvBridge()


    def callback_image(self, msg: Image):
        try:
            # Conver ROS2 Image message to OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # --- OPTIONAL ---
            # Process the image (conver to grayscale, rotate, etc)
            gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

            # Display the image
            cv2.imshow("Processed Image", cv_image)
            cv2.waitKey(1)

        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")


def main(args=None):
	rclpy.init(args=args)
	node = ImageSubscriber()
	
	rclpy.spin(node)
	rclpy.shutdown()

if __name__ == '__main__':
	main()