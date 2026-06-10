# ros2_perception

A collection of ROS2 perception nodes built with OpenCV and Python.
Each package demonstrates a different concept in robot perception — from basic image processing to object detection.

## Packages
| Package | Description |
|---|---|
| `image_processing` | Image subscriber, cv_bridge, basic OpenCV operations |

## 01 Image Processing
Basic ROS2 image pipeline — subscribing to a camera topic and processing frames with OpenCV.

### RUN
#### Terminal 1 - Start the camera publisher:
```bash
ros2 run image_tools cam2image
```

#### Terminal 2 - Start the image subscriber node:
```bash
ros2 run image_processing image_node
```

#### Topics
| Topic | Type | Description |
| --- | --- | --- |
| '/image' | 'sensor_msgs/Image' | Raw image from camera