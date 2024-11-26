from csi import CSIDataCollector
import rclpy

def main():
    # Initialize the ROS 2 Python client library
    rclpy.init()

    # Create the data collector node with or without video
    collector = CSIDataCollector(is_video=True)

    try:
        # Begin spinning the node to collect data
        print("Started data collection")
        rclpy.spin(collector)

    except KeyboardInterrupt:
        print("Data collection interrupted by user")

    finally:
        # Save collected data and perform cleanup
        collector.save()
        collector.destroy_node()
        
        # Only shutdown if rclpy is still active
        if rclpy.ok():
            rclpy.shutdown()
        print("Data collection and ROS shutdown completed.")

if __name__ == "__main__":
    main()
