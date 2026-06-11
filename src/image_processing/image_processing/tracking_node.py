#!/usr/bin/env python3

"""
ROS2 OBJECT TRACKING NODE

This node subscribes to the '/image' and track objects.
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort


class ObjectTrackingNode(Node):
    def __init__(self):
        super().__init__('object_tracking')

        # Subscriber to read raw image
        self.subscription_ = self.create_subscription(
            Image,
            '/image',
            self.callback_image,
            10
        )

        # Bridge to cover OpenCV images and ROS msgs
        self.bridge = CvBridge()
        # Load YOLO model with paramteres
        self.model = YOLO('yolov8n.pt')
        # Tracker
        self.tracker = DeepSort(max_age=30)


    def callback_image(self, msg: Image):
        try:
            # Conver ROS2 Image message to OpenCV image
            cv_frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # --- YOLO OBJECT DETECTION ---
            # Perform object detection
            detection_results = self.model(cv_frame)[0] # Get result for first image in the batch
            
            # Extracting bouding boxes and confidence scores
            detections = []
            for box in detection_results.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()      # Get bounding box coordinates
                confidence = float(box.conf[0])            # Get confidence score
                class_id = int(box.cls[0])                 # Get class ID
                detections.append(([x1, y1, float(x2-x1), float(y2-y1)],
                                   confidence,
                                   class_id)
                )

            # Update tracker with new detections
            tracks = self.tracker.update_tracks(detections, frame=cv_frame)

            # Draw bounded boxes and tracks IDs on the frame
            for track in tracks:
                 if not track.is_confirmed():
                      continue
                 
                 track_id = track.track_id
                 x1, y1, w, h = track.to_tlwh() # Get bounding boxes in (x, y, width, heigh) format
                 cv2.rectangle(cv_frame,
                               (int(x1), int(y1)), (int(x1 + w), int(y1 + h)),
                               (0, 255, 0),
                               2
                )
                 cv2.putText(cv_frame,
                            f'ID: {track_id}',
                            (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                            2
                )
                 
            # Display the result frame
            cv2.imshow('Object Tracking', cv_frame)
            cv2.waitKey(1)

        except Exception as e:
            # self.get_logger().error(f"Error processing image: {e}")
            import traceback
            self.get_logger().error(f"Error processing image: {traceback.format_exc()}")


def main(args=None):
	rclpy.init(args=args)
	node = ObjectTrackingNode()
	
	rclpy.spin(node)
	rclpy.shutdown()

if __name__ == '__main__':
	main()