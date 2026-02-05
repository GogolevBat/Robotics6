import asyncio
from enum import Enum

from pydantic import BaseModel
import json
if __name__ == "__main__":
    from app.moduleB import ModuleBWindow

class Coordinates(Enum):
    UNDER_CONV=(0.1, 0.0, 0.0, 0.0, 0.0, 0.0)
    TAKE_POS=(0.2, 0.0, 0.0, 0.0, 0.0, 0.0)

    TOOL_ON="self.win.robot.addToolState(1)"
    TOOL_OFF="self.win.robot.addToolState(0)"

    ROTATE_DEFECT=(0.5, 0.0, 0.0, 0.0, 0.0, 0.0)
    PLACE_DEFECT=(0.6, 0.0, 0.0, 0.0, 0.0, 0.0)

    ROTATE_CONV="self.win.robot.addLinearTrackMove(0)"
    ROTATE_PALETE_1="self.win.robot.addLinearTrackMove(0.2)"
    ROTATE_PALETE_2="self.win.robot.addLinearTrackMove(0.3)"
    ROTATE_PALETE_3="self.win.robot.addLinearTrackMove(0.4)"
    ROTATE_PALETE_4="self.win.robot.addLinearTrackMove(0.5)"
    
    CHOOSE_PLACE="НУЖНО ВЫБРАТЬ МЕСТО"
    UNDER_PLACES=(0.7, 0.0, 0.0, 0.54, 0.2, 0.1) 
    PLACE_1=(0.7, 0.0, 0.0, 0.0, 0.0, 0.0)
    PLACE_2=(0.8, 0.0, 0.0, 0.0, 0.0, 0.0)
    PLACE_3=(0.0, 0.3, 0.0, 0.0, 0.0, 0.0)
    PLACE_4=(0.0, 0.4, 0.0, 0.0, 0.0, 0.0)

class Palete:
    def __init__(self):
        self.all_clear()
        self.clear_count()
        self.max_field = 4

    def all_clear(self):
        self.places = {
            "1":0,
            "2":0,
            "3":0,
            "defect":0
        }
    def clear_count(self):
        self.counts = {
            "1":0,
            "2":0,
            "3":0,
            "defect":0
        }

    def clear(self, name):
        self.places[name] = 0

    def isempty(self, name):
        if name == "defect":
            return 0
        if self.places[name] >= self.max_field:
            return False
        return self.places[name] + 1
    
    def put(self, name):
        if name != "defect":
            self.places[name] += 1
        self.counts[name] += 1
        return True
    
    def show(self):
        return {
            "columns": ["Занятые места","Перенесено"],
            "matrix": list(zip(self.places.values(), self.counts.values())),
            "indexes": ["Объект 1", "Объект 2", "Объект 3", "БРАК", ],
        }

class OneAction(BaseModel):
    name: str
    actions: list[Coordinates]
    index_object: str = "defect"
    
    def dumps(self):
        return {
                "name": self.name,
                "actions": [act.name for act in self.actions],
                "index_object": self.index_object
            }

    @classmethod
    def loads(cls, data: dict):
        return cls(
            name=data["name"],
            actions=[getattr(Coordinates, act) for act in data["actions"]],
            index_object=data["index_object"]
        )

class AutomaticModule:
    def __init__(self, win: "ModuleBWindow"):
        self.algoritm: list[OneAction] = []
        self.palete = Palete()
        self.task: asyncio.Task = None
        self.log = win.log
        self.win = win

    def show(self):
        return {
            "columns": ["Объект"],
            "matrix": [[alg.name] for alg in self.algoritm],
        }
    
    def add(self, name):
        if name == "defect":
            self.algoritm.append(
                OneAction(
                name="БРАК",
                actions=[
                    Coordinates.UNDER_CONV,
                    Coordinates.TAKE_POS,
                    Coordinates.TOOL_ON,
                    Coordinates.UNDER_CONV,
                    Coordinates.ROTATE_DEFECT,
                    Coordinates.PLACE_DEFECT,
                    Coordinates.TOOL_OFF,
                    Coordinates.ROTATE_DEFECT,
                    Coordinates.UNDER_CONV
                ]
                )
            )
        else:
            self.algoritm.append(
                OneAction(
                name=f"Объект {name}",
                index_object = name,
                actions=[
                    Coordinates.UNDER_CONV,
                    Coordinates.TAKE_POS,
                    Coordinates.TOOL_ON,
                    Coordinates.UNDER_CONV,
                    getattr(Coordinates, f"ROTATE_PALETE_{name}"),
                    Coordinates.UNDER_PLACES,
                    Coordinates.CHOOSE_PLACE,                    
                    Coordinates.TOOL_OFF,
                    Coordinates.UNDER_PLACES,
                    Coordinates.ROTATE_CONV,
                    Coordinates.UNDER_CONV
                ]
                )
            )
        
    
    def remove(self):
        if len(self.algoritm):
            self.algoritm.pop()
    
    def clear(self):
        self.algoritm = []
    
    def create_one_action(self, one_action: OneAction):
        self.log.info(f"Идет загрузка действия в робота '{one_action.name}'")
        object_place = self.palete.isempty(one_action.index_object)

        if object_place is False:
            return None
        self.log.debug("Выбрано место", object_place)

        for action in one_action.actions:
            if action.name == "CHOOSE_PLACE":
                self.win.robot.addMoveToPointJ(getattr(Coordinates, f"PLACE_{object_place}"))
            elif isinstance(action.value, str):
                eval(action.value)
            else:
                self.win.robot.addMoveToPointJ(action.value) # Waypoint()
            self.win.robot.addWait(0.8)

        self.log.info(f"Выполнение действия '{one_action.name}'")
        self.win.robot.play()
        return True
    
    async def runner(self):
        try:
            
            self.log.info("Начало выполнения задания")
            index = 0
            emerg_flag = True
            self.win.lamp.green()
            flag_green = True
            while index < len(self.algoritm):
                await asyncio.sleep(0.5)
                one_action: OneAction = self.algoritm[index]
                result = await asyncio.to_thread(self.create_one_action, one_action)
                if result is None:
                    if emerg_flag:
                        self.log.error("Нет места для объекта", one_action.name)
                        self.win.lamp.red()
                    else:
                        self.win.lamp.clear()
                    flag_green = False
                    emerg_flag = not emerg_flag
                    continue
                elif not flag_green:
                    self.win.lamp.green()
                
                self.palete.put(one_action.index_object)

                index += 1
                # while not (await asyncio.to_thread(self.win.robot.getActualStateOut) is InterpreterStates.PROGRAM_IS_DONE.value):
                #   asyncio.sleep(0.1)
            self.log.info("Самостоятельная остановка алгоритма автоматизации")

        except asyncio.CancelledError:
            self.log.info("Принудительное прерывание задачи")
        except Exception as e:
            self.log.error("Ошибка при выполнении задания", e)
        finally:     
            try:       
                await asyncio.to_thread(self.win.robot.stop)
                await asyncio.to_thread(self.win.robot.reset)
            except:
                ...
            self.log.info("Окончание алгоритма")
            self.task = None
    
    def start(self):
        if self.task is None:
            self.task = asyncio.create_task(self.runner())
        
    def stop(self):
        if not self.task is None:
            self.task.cancel()

    def save(self):
        return [alg.dumps() for alg in self.algoritm]

    def load(self, data):
        self.algoritm = [OneAction.loads(alg) for alg in data]