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

from ultralytics import YOLO

class YoloDetectionNode(Node):
    def __init__(self):
        super().__init__('yolo_detection')

        # Subscriber to read raw image
        self.subscription_ = self.create_subscription(
            Image,
            '/image',
            self.callback_image,
            10
        )

        self.bridge = CvBridge()

        # Load YOLO model with paramteres
        self.model = YOLO('yolov8n.pt')


    def callback_image(self, msg: Image):
        try:
            # Conver ROS2 Image message to OpenCV image
            cv_frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # --- YOLO OBJECT DETECTION ---
            detection = self.model(cv_frame)
            annoted_frame = detection[0].plot()
            
            # Display the image
            cv2.imshow("YOLO Detection", annoted_frame)
            cv2.waitKey(1)

        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")


def main(args=None):
	rclpy.init(args=args)
	node = YoloDetectionNode()
	
	rclpy.spin(node)
	rclpy.shutdown()

if __name__ == '__main__':
	main()

