import pyb
from pyb import Pin
from staccel import STAccel
from sc1602 import SC1602

lcd_pin = {
    'RS': Pin.board.PB8,
    'E': Pin.board.PB9,
    'DB0': Pin.board.PE6,
    'DB1': Pin.board.PC13,
    'DB2': Pin.board.PE4,
    'DB3': Pin.board.PE5,
    'DB4': Pin.board.PB4,
    'DB7': Pin.board.PB7,
    'DB6': Pin.board.PD7,
    'DB5': Pin.board.PB5,
}

accel = STAccel()
lcd = SC1602(lcd_pin)

lcd.initialize()

while True:
    x, y, z = accel.xyz()
    lcd.set_cursor(0, 0)
    lcd.write("X:{0:+5.02f} Y:{1:+5.02f} ".format(x, y))
    lcd.set_cursor(1, 0)
    lcd.write("Z:{0:+5.02f}        ".format(z))
    pyb.delay(100)
