"""
MicroPython max7219 cascadable 8x8 LED matrix driver

Licensed under MIT, found in LICENSE.txt
    Copyright (c) 2017 Mike Causer
    Copyright (c) 2022 Leo Spratt
"""
from micropython import const
from framebuf import FrameBuffer, MONO_HLSB

_NOOP = const(0)
_DIGIT0 = const(1)
_DECODEMODE = const(9)
_INTENSITY = const(10)
_SCANLIMIT = const(11)
_SHUTDOWN = const(12)
_DISPLAYTEST = const(15)


class Matrix8x8(FrameBuffer):
    def __init__(self, spi, cs, num):
        """
        Driver for cascading MAX7219 8x8 LED matrices.

        >>> from machine import Pin, SPI
        >>> from max7219 import Matrix8x8
        >>> spi = SPI(1)
        >>> display = Matrix8x8(spi, Pin('X5'), 4)
        >>> display.text('1234',0,0,1)
        >>> display.show()

        """
        self.spi = spi
        self.cs = cs
        self.cs.init(cs.OUT, True)
        self.buffer = bytearray(8 * num)
        self.num = num

        super().__init__(self.buffer, 8 * num, 8, MONO_HLSB)

        self.init()

    def _write(self, command, data):
        self.cs(0)
        for _ in range(self.num):
            self.spi.write(bytearray([command, data]))
        self.cs(1)

    def init(self):
        for command, data in (
            (_SHUTDOWN, 0),
            (_DISPLAYTEST, 0),
            (_SCANLIMIT, 7),
            (_DECODEMODE, 0),
            (_SHUTDOWN, 1),
        ):
            self._write(command, data)

    def brightness(self, value):
        if not 0 <= value <= 15:
            raise ValueError("Brightness out of range")
        self._write(_INTENSITY, value)

    def show(self):
        for y in range(8):
            self.cs(0)
            for m in range(self.num):
                self.spi.write(bytearray([_DIGIT0 + y, self.buffer[(y * self.num) + m]]))
            self.cs(1)
