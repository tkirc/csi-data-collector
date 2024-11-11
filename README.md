# CSI Data Collector

This docker container saves all the data from the topics /wifi/csi and /wifi/realsense/color/image_raw for a specified number of seconds.
The saved .npy and .mp4 file can then in a next step be run through the detectron2 model to generate the ground truth.

To start the recording process use the following command:
```python3 main.py --duration 900 --video```
