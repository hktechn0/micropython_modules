import pyb
from pyb import Pin
from pyb import SPI

class SC1602:
    sc1602pin_default = {
        'RS': Pin.board.PE4,
        'E': Pin.board.PE5,
        'DB0': Pin.board.PE7,
        'DB1': Pin.board.PE8,
        'DB2': Pin.board.PE9,
        'DB3': Pin.board.PE10,
        'DB4': Pin.board.PE11,
        'DB5': Pin.board.PE12,
        'DB6': Pin.board.PE13,
        'DB7': Pin.board.PE14,
    }

    def __init__(self, pin=None):
        Pin.dict(pin or self.sc1602pin_default)
        self.rs = Pin("RS", Pin.OUT_PP)
        self.e = Pin("E", Pin.OUT_PP)
        self.db0 = Pin("DB0", Pin.OUT_PP)
        self.db1 = Pin("DB1", Pin.OUT_PP)
        self.db2 = Pin("DB2", Pin.OUT_PP)
        self.db3 = Pin("DB3", Pin.OUT_PP)
        self.db4 = Pin("DB4", Pin.OUT_PP)
        self.db5 = Pin("DB5", Pin.OUT_PP)
        self.db6 = Pin("DB6", Pin.OUT_PP)
        self.db7 = Pin("DB7", Pin.OUT_PP)

        self.e.low()

    def initialize(self):
        for _ in range(3):
            self.rs.low()
            self.__set_databus(0x30)
            self.__enable()
            pyb.delay(5)
        
        # function set
        self.rs.low()
        self.__set_databus(0x38)
        self.__enable()

        self.display_on_off(False)
        self.clear()
        self.display_on_off(True)

        # entry mode set
        self.rs.low()
        self.__set_databus(0x06)
        self.__enable()

    def __set_databus(self, data):
        self.db0.value(data & 1)
        self.db1.value((data >> 1) & 1)
        self.db2.value((data >> 2) & 1)
        self.db3.value((data >> 3) & 1)
        self.db4.value((data >> 4) & 1)
        self.db5.value((data >> 5) & 1)
        self.db6.value((data >> 6) & 1)
        self.db7.value((data >> 7) & 1)

    def __enable(self):
        self.e.high()
        pyb.udelay(1)
        self.e.low()
        pyb.udelay(40)

    def clear(self):
        self.rs.low()
        self.__set_databus(1)
        self.__enable()
        pyb.udelay(1600)

    def cursor_at_home(self):
        self.rs.low()
        self.__set_databus(2)
        self.__enable()
        pyb.udelay(1600)

    def display_on_off(self, display, cursor=False, blink=False):
        self.rs.low()
        self.__set_databus(8)

        if display:
            self.db2.high()
        if cursor:
            self.db1.high()
        if blink:
            self.db0.high()

        self.__enable()

    def set_cursor(self, y, x=0):
        self.rs.low()
        self.__set_databus((y * 0x40 + x) | 0x80)
        self.__enable()

    def putc(self, c):
        self.rs.high()
        self.__set_databus(ord(c))
        self.__enable()

    def write(self, string):
        for c in string:
            self.putc(c)

if __name__ == "__main__":
    import sc1602
    lcd = sc1602.SC1602()
    lcd.initlalize()
    lcd.write("Hello, world!")
    lcd.set_cursor(1, 0)
    lcd.write("Micro Python")
