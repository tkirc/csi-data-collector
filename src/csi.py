import numpy as np
import time
import cv2
import rclpy
from rclpy.node import Node
from wifi_detection_interfaces.msg import CsiData
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from collections import deque

class CSIDataCollector(Node):
    def __init__(self, is_video=False):
        super().__init__('csi_data')
        self._data = []
        self.csi_data = []
        self.video_frames = []
        self.buffer = deque(maxlen=5)

        
        # Initialize ROS2 subscribers
        self.csi_subscription = self.create_subscription(
            CsiData,
            '/wifi/csi',
            self.csi_data_callback,
            1
        )

        if is_video:
            self.video_subscription = self.create_subscription(
                Image,
                '/wifi/realsense/color/image_raw',
                self.camera_callback,
                1
            )
            self.bridge = CvBridge()
            self.video = True
        else:
            self.video = False

    def csi_data_callback(self, msg):
        # Speichern aller empfangenen Werte in einem Dictionary
        csi_data_dict = {
            'time_stamp': msg.time_stamp,
            'csi_len': msg.csi_len,
            'channel': msg.channel,
            'err_info': msg.err_info,
            'noise_floor': msg.noise_floor,
            'rate': msg.rate,
            'band_width': msg.band_width,
            'num_tones': msg.num_tones,
            'nr': msg.nr,
            'nc': msg.nc,
            'rssi': msg.rssi,
            'rssi_1': msg.rssi_1,
            'rssi_2': msg.rssi_2,
            'rssi_3': msg.rssi_3,
            'payload_len': msg.payload_len,
            'payload': list(msg.payload),  # Konvertiere zu einer Liste, da es ein Array sein kann
        }

        # CSI-Daten als komplexe Zahlen speichern
        csi_data_dict['csi_complex'] = [
            complex(real, imag) for real, imag in zip(msg.csi_real, msg.csi_imag)
        ]

        # CSI-Daten reshapen zu 3x3x114
        csi_complex_reshaped = np.array(csi_data_dict['csi_complex']).reshape(3, 3, 114)

        # Zuschnitt auf 3x3x56
        csi_complex_trimmed = csi_complex_reshaped[:, :, :56]

        # Transponieren zu 56x3x3
        csi_complex_transposed = np.transpose(csi_complex_trimmed, (2, 0, 1))
        
        self.buffer.append(csi_complex_transposed)

    def camera_callback(self, msg):
        """Callback to handle incoming camera frames from the ROS2 topic."""
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        if len((list(self.buffer))) == 5:
            self.csi_data.append(np.concatenate(list(self.buffer), axis=0))
            self.video_frames.append(frame)

    def collect_csi_data(self, duration=60):
        """Collects CSI data and video frames for the specified duration."""
        start_time = time.time()
        while time.time() - start_time < duration:
            rclpy.spin_once(self, timeout_sec=0.01)  # Non-blocking
        #return self.csi, self.video_frames

    def save(self, csi_filename='csi_data.npy', video_filename='video_frames.mp4'):
        """Saves the CSI data and video frames to files."""
        
        # Save CSI data
        if self.csi_data:
            np.save(csi_filename, self.csi_data)
            print(f"CSI data saved to {csi_filename}")
        else:
            print("No CSI data to save.")

        # Save video frames
        if self.video_frames:
            frame_height, frame_width = self.video_frames[0].shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(video_filename, fourcc, 30, (frame_width, frame_height))

            for frame in self.video_frames:
                out.write(frame)

            out.release()
            print(f"Video frames saved to {video_filename}")
        else:
            print("No video frames to save.")