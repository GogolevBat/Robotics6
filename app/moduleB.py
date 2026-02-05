import datetime
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import *
from numpy import delete
from utils.mlamp import MyLamp, NoneLamp
from utils.mlogger import Logger
from qasync import QApplication, QEventLoop, asyncSlot
import asyncio
from utils.fake_motion import RobotControl
from moduleA import ModuleAWindow
import csv
import pandas
from utils.algoritm import AutomaticModule
import json

class AutoAddObject(QObject):
    def __init__(self, win: "ModuleBWindow", name):
        super().__init__()
        self.win = win
        self.name = name
    def action(self):
        self.win.auto.add(self.name)

class AutoClearObject(QObject):
    def __init__(self, win: "ModuleBWindow", name):
        super().__init__()
        self.win = win
        self.name = name
    def all_clear(self):
        self.win.auto.palete.all_clear()
    def clear(self):
        self.win.auto.palete.clear(self.name)

class ModuleBWindow(ModuleAWindow):
    def __init__(self):
        super().__init__()
        self.auto = AutomaticModule(self)


    def start_ui(self):
        super().start_ui()
        self.auto_actions = [
                AutoAddObject(self, "1"),
                AutoAddObject(self, "2"),
                AutoAddObject(self, "3"),
                AutoAddObject(self, "defect"),
            ]
        self.ui.auto_object_1.clicked.connect(self.auto_actions[0].action)
        self.ui.auto_object_2.clicked.connect(self.auto_actions[1].action)
        self.ui.auto_object_3.clicked.connect(self.auto_actions[2].action)
        self.ui.auto_object_defect.clicked.connect(self.auto_actions[3].action)

        self.auto_actions_clear = [
                AutoClearObject(self, "1"),
                AutoClearObject(self, "2"),
                AutoClearObject(self, "3"),
                AutoClearObject(self, ""),
            ]
        self.ui.auto_clear_palete_1.clicked.connect(self.auto_actions_clear[0].clear)
        self.ui.auto_clear_palete_2.clicked.connect(self.auto_actions_clear[1].clear)
        self.ui.auto_clear_palete_3.clicked.connect(self.auto_actions_clear[2].clear)
        self.ui.auto_clear_palete_all.clicked.connect(self.auto_actions_clear[3].all_clear)

        self.ui.auto_delete.clicked.connect(self.delete_algoritm)
        self.ui.auto_start.clicked.connect(self.start_algoritm)
        self.ui.auto_stop.clicked.connect(self.stop_algoritm)
        self.ui.auto_clear.clicked.connect(self.clear_algoritm)
        self.ui.auto_clear_palete_all_2.clicked.connect(self.clear_count)

        self.ui.emergancy_stop.clicked.connect(self.emergency_stop)

        self.ui.auto_save_button.clicked.connect(self.automatic_save)
        self.ui.auto_load_button.clicked.connect(self.automatic_load)

    def clear_count(self):
        self.auto.palete.clear_count()

    def automatic_save(self):
        filename, _ = QFileDialog.getSaveFileName()
        if filename:
            with open(f"{filename}.json", "w") as f:
                json.dump(self.auto.save(), f, indent=4, ensure_ascii=False)
    
    def automatic_load(self):
        filename, _ = QFileDialog.getOpenFileName()
        if filename:
            with open(f"{filename}", "r") as f:
                self.auto.load(json.load(f))

    @asyncSlot()
    async def emergency_stop(self):
        self.log.error("Экстренная остановка")
        self.auto.stop()
        await asyncio.to_thread(self.robot.reset)
        await self.manual_conv_stop()
        self.lamp.red()

    def delete_algoritm(self):
        self.auto.remove()
    def stop_algoritm(self):
        self.auto.stop()
    def start_algoritm(self):
        self.auto.start()
    def clear_algoritm(self):
        self.auto.clear()

    def pause(self):
        super().pause()
        self.auto.stop()
    
    async def lifespan(self):
        await super().lifespan()

        self.update_table(
            self.ui.auto_table_palete_information,
            **self.auto.palete.show()
        )
        self.update_table(
            self.ui.auto_table_algoritm,
            **self.auto.show()
        )

async def main(win: ModuleBWindow, event: asyncio.Event):
    while not event.is_set():
        await asyncio.sleep(.5)
        await win.lifespan()


if __name__ == "__main__":
    import sys
    event = asyncio.Event()
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(event.set)
    win = ModuleBWindow()
    win.show()
    asyncio.run(main(win, event), loop_factory=QEventLoop)