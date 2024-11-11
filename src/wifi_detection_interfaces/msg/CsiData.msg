# Filename: CsiData.msg

# Single values
uint64 time_stamp
uint16 csi_len
uint16 channel
uint8 err_info
uint8 noise_floor
uint8 rate
uint8 band_width
uint8 num_tones
uint8 nr
uint8 nc
uint8 rssi
uint8 rssi_1
uint8 rssi_2
uint8 rssi_3
uint16 payload_len

# Arrays for CSI data. Since complex numbers are not directly supported,
# each complex element is stored as two separate elements (real and imaginary parts)
# in two parallel arrays.
float64[] csi_real
float64[] csi_imag

# Payload
uint8[] payload