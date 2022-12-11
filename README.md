# MicroPython Max7219 8x8 LED Matrix
A MicroPython library for the MAX7219 8x8 LED matrix driver using the SPI interface.Supports cascading matrices extending the [framebuf](http://docs.micropython.org/en/latest/pyboard/library/framebuf.html) class.


## Examples
### Raspberry Pi Pico

| Pico      | max7219 |
| :-------- | :------ |
| 40 (VBUS) | VCC 5V  |
| 38 (GND)  | GND     |
| 5 (GP3)   | DIN     |
| 7 (GP5)   | CS      |
| 4 (GP2)   | CLK     |

```python
from machine import Pin, SPI
from max7219 import Matrix8x8

spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)

display = Matrix8x8(spi, ss, 4)

display.brightness(5)

display.fill(0)
display.show()

display.text("CODE")
display.show()
```


## Attribution
- Original code by [@mcauser](https://github.com/mcauser/micropython-max7219)


## License
Licensed under the [MIT License](http://opensource.org/licenses/MIT), found in `LICENSE.txt`.
