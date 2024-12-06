import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


import cv2
import numpy as np

# Load the MobileNet SSD model
net = cv2.dnn.readNetFromCaffe(
    "/home/ubu/ros2_caffe/src/py_pubsub/py_pubsub/MobileNetSSD_deploy.prototxt.txt",
    "/home/ubu/ros2_caffe/src/py_pubsub/py_pubsub/MobileNetSSD_deploy.caffemodel"
)

# Object classes
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

def detect_objects(frame):
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, 
        (300, 300), 127.5)
    
    net.setInput(blob)
    detections = net.forward()
    
    results = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:
            class_id = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            results.append((class_id, confidence, (startX, startY, endX, endY)))
    
    return results

def calculate_distance(known_width, focal_length, pixel_width):
    return (known_width * focal_length) / pixel_width

class MinimalPublisher(Node):

    def __init__(self, label, distance):
        super().__init__('minimal_publisher')
        self.declare_parameter('frame_id', '')
        self.frame_id = str(self.get_parameter('frame_id').value)
        
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        
        self.timer = self.create_timer(0.2, self.timer_callback(label, distance))

    def timer_callback(self, label, distance):
        if label == "bottle":
            print("bot")
            print(distance)
            if distance < 5:
                twists = Twist()
                twists.linear.x = 0.0
                self.publisher_.publish(twists)
                print("stop")
            else:
                twists = Twist()
                twists.linear.x = 0.1
                self.publisher_.publish(twists)
                print('go')

def main(args=None):

    rclpy.init(args=args)

    cap = cv2.VideoCapture(0)
    
    # Constants for distance calculation
    KNOWN_WIDTHS = {
        "bottle": 3.0,  # inches
        "person": 18.0,
        "chair": 16.0
    }
    FOCAL_LENGTH = 350
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        detections = detect_objects(frame)
        
        for (class_id, confidence, box) in detections:
            (startX, startY, endX, endY) = box
            label = CLASSES[class_id]
            
            pixel_width = endX - startX
            if label in KNOWN_WIDTHS:
                distance = calculate_distance(KNOWN_WIDTHS[label], FOCAL_LENGTH, pixel_width)
                label2 = f"{label}: {distance:.1f} inches"
            minimal_publisher = MinimalPublisher(label, distance)
            
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                         COLORS[class_id].tolist(), 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label2, (startX, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[class_id].tolist(), 2)
        
        cv2.imshow("Object Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()