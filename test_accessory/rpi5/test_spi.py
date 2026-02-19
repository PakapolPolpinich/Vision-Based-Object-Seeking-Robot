import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 1)     # bus 0, CE1

spi.mode = 0b00
spi.max_speed_hz = 500000
spi.bits_per_word = 8

print("SPI Running...")

while True:
    tx = [ord('s'), ord('h'), ord('e')]
    rx = spi.xfer2(tx)

    print("TX:", tx)
    print("RX:", rx)

    time.sleep(1)