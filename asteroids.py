# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_lis3dh
import displayio
import framebufferio
import rgbmatrix
import terminalio
import math
import random

# accellerometer setup
# PyGamer or MatrixPortal I2C Setup:
i2c = board.I2C()  # uses board.SCL and board.SDA
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)
# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_2_G

# matrix setup
displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64, height=64, bit_depth=6,
    rgb_pins=[board.MTX_R1, board.MTX_G1, board.MTX_B1, board.MTX_R2, board.MTX_G2, board.MTX_B2],
    addr_pins=[board.MTX_ADDRA, board.MTX_ADDRB, board.MTX_ADDRC, board.MTX_ADDRD, board.MTX_ADDRE],
    clock_pin=board.MTX_CLK, latch_pin=board.MTX_LAT, output_enable_pin=board.MTX_OE)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)
g = displayio.Group()
bitmap = displayio.Bitmap(64, 64, 4)
palette = displayio.Palette(4)
palette[0] = 0x000000
palette[1] = 0xFF0000
palette[2] = 0x00FF00
palette[3] = 0x0000FF
bitmap[31,31]=1
tg = displayio.TileGrid(bitmap=bitmap, pixel_shader=palette)
g.append(tg)
display.show(g)

# Loop forever printing accelerometer values

asteroidsX = [2,17,30,42]
asteroidsY = [0,0,0,0]
speeds = [1,2,3,1]
while True:
    # Read accelerometer values (in m / s ^ 2).  Returns a 3-tuple of x, y,
    # z axis values.  Divide them by 9.806 to convert to Gs.
    x, y, z = [
        value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration
    ]
    
    bitmap.fill(0x000000)
    
    # accelerometer
    X = math.floor((x+1.0)/2.0*64.0)
    if X > 63:
        X = 63
    if X < 0:
        X = 0
    Y = math.floor((y+1.0)/2.0*64.0)
    if Y > 63:
        Y = 63
    if Y < 0:
        Y = 0
    bitmap[X,Y] = 1
    
    # background
    for i,a in enumerate(asteroidsX):
        newpos = asteroidsY[i] + speeds[i]
        if newpos < 64:
            asteroidsY[i] = newpos
            bitmap[a, asteroidsY[i]] = 3
            #if X == asteroidsX[i] and Y == asteroidsY[i]:
            #    time.sleep(100000)
        else:
            asteroidsX[i] = math.floor(random.random()*64)
            asteroidsY[i] = 0
            speeds[i] = math.floor(1 + random.random()*3)
            #if X == asteroidsX[i] and Y == asteroidsY[i]:
            #    time.sleep(100000)
            
    display.refresh(minimum_frames_per_second=0)



