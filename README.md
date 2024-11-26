# CSI Data Collector

This docker container saves all the data from the topics /wifi/csi and /wifi/realsense/color/image_raw until its interrupted by the user.
The saved .npy and .mp4 file can then in a next step be run through the detectron2 model to generate the ground truth.

To start the recording process use the following command:
```python3 main.py```

Interrupt the recording with ```ctrl + c```
