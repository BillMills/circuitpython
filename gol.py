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

# matrix setup
displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64, height=64, bit_depth=6,
    rgb_pins=[board.MTX_R1, board.MTX_G1, board.MTX_B1, board.MTX_R2, board.MTX_G2, board.MTX_B2],
    addr_pins=[board.MTX_ADDRA, board.MTX_ADDRB, board.MTX_ADDRC, board.MTX_ADDRD, board.MTX_ADDRE],
    clock_pin=board.MTX_CLK, latch_pin=board.MTX_LAT, output_enable_pin=board.MTX_OE)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

dim = 64
g = displayio.Group()
bitmap = displayio.Bitmap(64, 64, 4)
buffer = []
for i in range(64):
    buffer.append([])
    for j in range(64):
        buffer[i].append(0)
palette = displayio.Palette(4)
palette[0] = 0x000000
palette[1] = 0xFFFFFF
palette[2] = 0xf542ef
palette[3] = 0xFF0000
tg = displayio.TileGrid(bitmap=bitmap, pixel_shader=palette)
g.append(tg)
display.show(g)

for i in range(500):
    x = math.floor(random.random()*dim)
    y = math.floor(random.random()*dim)
    bitmap[x,y] = 1
    buffer[x][y] = 1

while True:
    display.refresh(minimum_frames_per_second=0)
    
    for x in range(dim):
        for y in range(dim):
            n = 0
            # counting neighbors
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if (i==0 and j==0) or (x + i) < 0 or (x + i) > dim-1 or (y + j) < 0 or (y + j) > dim-1:
                        continue
                    else:
                        n += bitmap[x+i,y+j]

            if bitmap[x,y] == 1:
                if n==2 or n==3:
                    buffer[x][y] = 1
                else:
                    buffer[x][y] = 0
            else:
                if n==3:
                    buffer[x][y] = 1
                    
    for X in range(dim):
        for Y in range(dim):
            bitmap[X,Y] = buffer[X][Y]
            #if bitmap[X,Y] == 3:
            #    bitmap[X,Y] = 0
            #if bitmap[X,Y] > 0 and bitmap[X,Y] < 3 and buffer[X][Y]==0:
            #    bitmap[X,Y] += 1
            #if buffer[X][Y] == 0:
            #    bitmap[X,Y] = 0
            #elif buffer[X][Y] == 1 and bitmap[X,Y] == 0:
            #    bitmap[X,Y] = 1
    display.refresh(minimum_frames_per_second=0)

