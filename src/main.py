import argparse
from csi import CSIDataCollector
import rclpy

def main(duration, video):
    # Initialize the CSIDataCollector
    rclpy.init()
    collector = CSIDataCollector(is_video=video)

    try:
        # Collect CSI data and video frames for the specified duration
        print("Started data collection")
        collector.collect_csi_data(duration=duration)

        # Check if both sets of data are the same length
        if len(collector.csi_data) == len(collector.video_frames):
            print("Both sets are the same length")
            print(f"Number of collected data points: {len(collector.csi_data)}")
        else:
            print("CSI data and video frames are not the same length")

        # Save the collected data
        collector.save()
        
    finally:
        # Clean up ROS node and shutdown
        collector.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="CSI Data Collector")
    parser.add_argument("--duration", type=int, default=600, help="Duration for data collection in seconds")
    parser.add_argument("--video", action="store_true", help="Enable video recording")
    
    args = parser.parse_args()
    
    # Run main with parsed arguments
    main(duration=args.duration, video=args.video)
