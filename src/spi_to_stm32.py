
import spidev

class SPIProtocol:

    def __init__(self, bus=0, device=1, speed=500000):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.mode = 0b00 #mode 0
        self.spi.max_speed_hz = speed
        self.spi.bits_per_word = 8

    def send(self, data_bytes):
        tx = list(data_bytes)
        rx = self.spi.xfer2(tx)
        return rx

    def close(self):
        self.spi.close()