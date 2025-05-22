from smbus2 import SMBus, i2c_msg
import time

class TFminiI2C:
    def __init__(self, I2Cbus, address):
        self.I2Cbus = I2Cbus
        self.address = address

    def readDistance(self):
        write = i2c_msg.write(self.address, [1, 2, 7])
        read = i2c_msg.read(self.address, 7)
        with SMBus(self.I2Cbus) as bus:
            bus.i2c_rdwr(write, read)
            data = list(read)
            distance = data[3] << 8 | data[2]
        return distance

    def reset(self):
        reset = i2c_msg.write(self.address, [0x06])
        with SMBus(self.I2bus) as bus:
            bus.i2c_rdwr(reset)
            time.sleep(0.05)

# LiDAR setup
LIDAR_LEFT = TFminiI2C(1, 0x30)
LIDAR_RIGHT = TFminiI2C(1, 0x11)
LIDAR_FRONT = TFminiI2C(1, 0x12)
LIDAR_DOWN = TFminiI2C(1, 0x10)

front_distance = LIDAR_FRONT.readDistance()
left_distance = LIDAR_LEFT.readDistance()
right_distance = LIDAR_RIGHT.readDistance()

# Overlay distances on the frame
if front_distance is not None:
    front_text = f"Front: {front_distance} cm"
    cv2.putText(frame, front_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
if left_distance is not None:
    left_text = f"Left: {left_distance} cm"
    cv2.putText(frame, left_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
if right_distance is not None:
    right_text = f"Right: {right_distance} cm"
    cv2.putText(frame, right_text, (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
