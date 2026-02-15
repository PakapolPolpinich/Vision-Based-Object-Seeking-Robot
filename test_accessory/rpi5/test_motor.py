import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 1)     # bus 0, CE1

spi.mode = 0b00
spi.max_speed_hz = 500000
spi.bits_per_word = 8

print("SPI Running...")

tx = ord('f')             # ???? 'f' ? ASCII (102)
rx = spi.xfer2([tx])      # ??????????? list

print("TX:", tx)
print("RX:", rx)

spi.close()
