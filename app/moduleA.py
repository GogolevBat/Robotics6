import datetime
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import *
from utils.mlamp import MyLamp, NoneLamp
from utils.mlogger import Logger
from designe import Ui_MainWindow
from qasync import QApplication, QEventLoop, asyncSlot
import asyncio
from utils.fake_motion import RobotControl
import csv
import pandas
class ManualMotion(QObject):
    def __init__(self, win: "ModuleAWindow", index: int, wig: QSlider):
        super().__init__()
        self.win =win
        self.index = index
        self.wig = wig
    
    @asyncSlot()
    async def joint(self):
        pos = self.win.state.current_position_joint.copy()
        pos[self.index] = (self.wig.value() - 5) * 0.01
        self.win.log.info(f"Ручное посуставное управление", pos)
        await asyncio.to_thread(self.win.robot.setJointVelocity, pos)
        
        if (self.wig.value() - 5) == 0:
            self.win.lamp.blue()
        else:
            self.win.lamp.green()

    @asyncSlot()
    async def linear(self):
        pos = self.win.state.current_position_linear.copy()
        print(pos)
        pos[self.index] = (self.wig.value() - 5) * 0.01
        self.win.log.info(f"Ручное линейное управление", pos)
        await asyncio.to_thread(self.win.robot.setCartesianVelocity, pos)
        
        if (self.wig.value() - 5) == 0:
            self.win.lamp.blue()
        else:
            self.win.lamp.green()

    def realese(self):
        self.wig.setValue(5)


class State:
    def __init__(self):
        self.clear()
        current_position_joint = None
        current_position_linear = None

    def set(self, name=None):
        dt = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        if not name is None:
            self.objects[name][0] += 1
            self.objects[name][1] = dt
        self.count += 1
        self.last_code = dt
    
    def show(self):
        return {
            "columns": ["Кол-во", "Время"],
            "matrix": [[self.count, self.last_code], *self.objects.values()],
            "indexes": ["Всего", "Брак", "Объект 1", "Объект 2", "Объект 3"]
        }

    def clear(self):
        self.objects = {
            "defect": [0, None],
            1: [0, None],
            2: [0, None],
            3: [0, None],
        }
        self.count = 0
        self.last_code = None

    
class ModuleAWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.start_ui()
        self.log = Logger(self.ui.logs_field)
        self.state = State()
        self.lamp = NoneLamp(self.log)


    def connect(self):
        self.robot = RobotControl()
        self.lamp = MyLamp(self.ui.lamp_field_state)

    def disconnect(self):
        self.robot = None
        self.state.current_position_joint = None
        self.state.current_position_linear = None
        self.lamp.clear()
        self.lamp = NoneLamp(self.log)

    def start_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.manual_actions = []
        for name, wig in self.ui.__dict__.items():
            if "manual_slider_joints_" in name and isinstance(wig, QSlider):
                act = ManualMotion(self, int(name[-1]), wig)
                wig.valueChanged.connect(act.joint)
                wig.sliderReleased.connect(act.realese)
                self.manual_actions.append(act)
            if "manual_slider_linear" in name and isinstance(wig, QSlider):
                act = ManualMotion(self, int(name[-1]), wig)
                wig.valueChanged.connect(act.linear)
                wig.sliderReleased.connect(act.realese)
                self.manual_actions.append(act)

        self.ui.connect_robot.clicked.connect(self.robot_connect)
        self.ui.disconnect_robot.clicked.connect(self.robot_disconnect)
        
        self.ui.main_action_field.currentChanged.connect(self.change_main_window)
        self.ui.manual_actions_window.currentChanged.connect(self.change_manual_window)

        self.ui.manual_conv_stop.clicked.connect(self.manual_conv_stop)
        self.ui.manual_conv_start.clicked.connect(self.manual_conv_start)

        self.ui.manual_gripper_on.clicked.connect(self.man_gripper_on)
        self.ui.manual_gripper_off.clicked.connect(self.man_gripper_off)
        
        self.ui.initial_position_button.clicked.connect(self.initial_pose)
        self.ui.pause.clicked.connect(self.pause)
        self.ui.robot_clear_motion.clicked.connect(self.pause)
        
        self.ui.manual_gripper_off_A.clicked.connect(self.man_gripper_off_A)
        self.ui.manual_gripper_off_B.clicked.connect(self.man_gripper_off_B)
        self.ui.manual_gripper_off_C.clicked.connect(self.man_gripper_off_C)
        self.ui.manual_gripper_off_defect.clicked.connect(self.man_gripper_off_defect)
        
        self.ui.manual_save_staet_for_objects.clicked.connect(self.manual_save_state)
        self.ui.logs_save_button.clicked.connect(self.save_logs)
        self.ui.manual_clear_state_for_objects.clicked.connect(self.manual_clear_state_for_objects)


    @asyncSlot()
    async def man_gripper_off_A(self):
        self.log.error("Экстренная остановка")
        await asyncio.to_thread(self.robot.reset)
        await self.manual_conv_stop()
        self.lamp.red()
        

    def manual_clear_state_for_objects(self):
        self.state.clear()
        self.log.info("Очистка состояния")

    def manual_save_state(self):
        filename, _  = QFileDialog().getSaveFileName()
        if filename:
            pandas.DataFrame([[self.state.count, self.state.last_code], *self.state.objects.values()], 
                             columns=["Кол-во", "Время"], 
                             index=["Всего", "Брак", "Объект 1", "Объект 2", "Объект 3"]
                             ).to_excel(f"{filename}.xlsx")

    
    
    @asyncSlot()
    async def man_gripper_off_A(self):
        await asyncio.to_thread(self.robot.toolOFF)
        self.state.set(1)
        self.log.info("Отпускание объекта A")
    @asyncSlot()
    async def man_gripper_off_B(self):
        await asyncio.to_thread(self.robot.toolOFF)
        self.state.set(2)
        self.log.info("Отпускание объекта Б")
    @asyncSlot()
    async def man_gripper_off_C(self):
        await asyncio.to_thread(self.robot.toolOFF)
        self.state.set(3)
        self.log.info("Отпускание объекта В")
    @asyncSlot()
    async def man_gripper_off_defect(self):
        await asyncio.to_thread(self.robot.toolOFF)
        self.state.set("defect")
        self.log.info("Отпускание объекта Брак")

    def save_logs(self):
        filename, _  = QFileDialog().getSaveFileName()
        if filename:
            with open(f"{filename}.csv", "w") as f:
                wcsv = csv.writer(f)
                wcsv.writerow(["Дата", "Уровень", "Сообщение"])
                wcsv.writerows(self.log.logs.values())
                f.flush()
    

    @asyncSlot()
    async def robot_clear_motion(self):
        await asyncio.to_thread(self.robot.reset)
        self.log.info("Сброс старой программы робота")

    @asyncSlot()
    async def man_gripper_on(self):
        await asyncio.to_thread(self.robot.toolON)
        self.log.info("Захват объекта")
    @asyncSlot()
    async def man_gripper_off(self):
        await asyncio.to_thread(self.robot.toolOFF)
        self.state.set()
        self.log.info("Отпускание объекта")

    @asyncSlot()
    async def manual_conv_stop(self):
        await asyncio.to_thread(self.robot.conveyer_stop)
        self.log.info("Остановка конвейера")

    @asyncSlot()
    async def manual_conv_start(self):
        await asyncio.to_thread(self.robot.conveyer_start)
        self.log.info("Запуск конвейера")
    

    def change_main_window(self):
        index = self.ui.main_action_field.currentIndex()
        if not hasattr(self, "robot"):
            self.ui.main_action_field.setCurrentIndex(0)
            self.log.warning("Перед управлением нужно подключить робота")
            return 

        if index > 0 and self.robot is None:
            self.ui.main_action_field.setCurrentIndex(0)
            self.log.warning("Перед управлением нужно подключить робота")
            return
        if index == 1:
            self.log.info("Включенно ручное управление!")
            self.ui.manual_actions_window.setCurrentIndex(0)
       
    @asyncSlot()
    async def change_manual_window(self):
        index = self.ui.manual_actions_window.currentIndex()
        if index == 1:
            await asyncio.to_thread(self.robot.manualJointMode)
            self.log.info("Посуставное ручное управление")
        else:
            await asyncio.to_thread(self.robot.manualCartMode)
            self.log.info("Линейное ручное управление")

    @asyncSlot()
    async def initial_pose(self):
        await asyncio.to_thread(self.robot.moveToInitialPose)
        self.lamp.blue()
        self.log.info("Возврат на начальную позицию")

    @asyncSlot()
    async def pause(self):
        await asyncio.to_thread(self.robot.reset)
        self.lamp.yellow()
        self.log.info("Инициализация паузы")

    def robot_connect(self):
        if hasattr(self, "robot"):
            if not self.robot is None:
                return
        self.log.info("Подключение к роботу")
        self.connect()

    def robot_disconnect(self):
        self.log.info("Отключение от робота")
        self.disconnect()

    def update_table(self, table: QTableWidget, columns: list, matrix: list[list], indexes = None):
        table.setRowCount(len(matrix))
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)
        if not indexes is None:
            table.setVerticalHeaderLabels(indexes)
        for x, row in enumerate(matrix):
            for y, el in enumerate(row):
                table.setItem(x, y, QTableWidgetItem(str(el)))

    def lifespan_(self):
        joint_state = []
        joint_state.append(self.robot.getMotorPositionRadians())
        self.state.current_position_joint = joint_state[0]
        joint_state.append(list(map(lambda x: x * 57.3, joint_state[0])))
        joint_state.append(self.robot.getMotorPositionTick())
        joint_state.append([self.robot.getActualTemperature()] * 6)

        mini_state: list = []
        position = self.robot.getToolPosition()
        mini_state.extend(position)
        self.state.current_position_linear = position
        mini_state.append(self.robot.getToolState())
        return joint_state, mini_state
                

    async def lifespan(self):
        
        if not hasattr(self, "robot"):
            return 
        if self.robot is None:
            return

        joint_state, mini_state = await asyncio.to_thread(self.lifespan_)

        self.update_table(
            self.ui.table_state_joints,
            ["j1","j2","j3","j4","j5","j6"],
            joint_state,
            ["Радианы","Градусы","Тики","Температура"]
        )
        self.update_table(
            self.ui.table_state_linear_mini,
            ["x","y","z","rx","ry","rz", "gripper"],
            [mini_state],
        )
        self.update_table(
            self.ui.manual_table_movement,
            **self.state.show()
        )

async def main(win: ModuleAWindow, event: asyncio.Event):
    while not event.is_set():
        await asyncio.sleep(.5)
        await win.lifespan()

if __name__ == "__main__":
    import sys
    event = asyncio.Event()
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(event.set)
    win = ModuleAWindow()
    win.show()
    asyncio.run(main(win, event), loop_factory=QEventLoop)
