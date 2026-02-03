import asyncio
from .fake_motion import LedLamp
from PyQt5.QtWidgets import QLabel
from .mlogger import Logger
class MyLamp(LedLamp):
    def __init__(self, field: QLabel, ip='192.168.2.101', port=8890):
        super().__init__(ip, port)
        self.field = field

    def _set(self, color="#ffffff", action: str="0000"):
        self.field.setStyleSheet(f"background-color: {color}")
        self.task = asyncio.create_task(asyncio.to_thread(self.setLamp, action))
    
    def red(self):
        self._set("#ff0000", "0001")
    def blue(self):
        self._set("#0000ff", "1000")
    def green(self):
        self._set("#00ff00", "0100")
    def yellow(self):
        self._set("#ffff00", "0010")
    def clear(self):
        self._set("#ffffff", "0000")

class NoneLamp:
    def __init__(self, log: Logger):
        self.log = log
    red = lambda self: self.log.info("Лампа отключена")
    blue = lambda self: self.log.info("Лампа отключена")
    green = lambda self: self.log.info("Лампа отключена")
    yellow = lambda self: self.log.info("Лампа отключена")
    clear = lambda self: self.log.info("Лампа отключена")


