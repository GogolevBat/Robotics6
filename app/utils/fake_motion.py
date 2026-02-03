import time
import random
from math import radians, pi

class Waypoint:
    def __init__(self, coords):
        self.coords = coords
        print(f"[FAKE] Waypoint создан: {coords}")

    def __repr__(self):
        return f"Waypoint({self.coords})"


class LedLamp:
    def __init__(self, ip='192.168.2.101', port=8890):
        self.status = "0000"
        print(f"[FAKE] LedLamp создана для IP {ip}:{port}")

    def setLamp(self, status):
        """
        Set light to the lamp.
            Args:
                state: status for each color

            Description:
                The status for the "state" variable is written in the sequence:
                  - 1111 to turn on all colors
                  - 0000 to turn off all colors 
            
                - The first digit corresponds (**1**000) -> blue color
                - The second digit corresponds (0**1**00) -> green color
                - The third digit corresponds (00**1**0) -> yellow color
                - The fourth digit corresponds (000**1**) -> red color
        
            Returns:
                bool: True if operation succeeded, False otherwise
        """
        if len(status) != 4 or not all(c in "01" for c in status):
            print("[FAKE][ERROR] Некорректный формат статуса лампы")
            return
        self.status = status
        print(f"[FAKE] Лампа установлена в состояние: {status}")


class RobotControl:
    def __init__(self, ip='192.168.2.100', port='5568:5567', login='*', password='*'):
        print(f"[FAKE] RobotControl инициализирован для IP {ip}:{port}")
        self.connected = False
        self.joint_mode = False
        self.cart_mode = False
        self.tool_on = False
        self.position = [0.0] * 6

    def connect(self):
        """
        Connect to the robot ARM
            Returns:
                bool: True if operation is completed, False if failed
            
        """
        self.connected = True
        print("[FAKE] Robot ARM connected successfully")
        return True
    
    def conveyer_start(self) -> bool:
        """
        Start motor to the conveyer
            Returns:
                bool: True if operation is completed, False if failed
        
        """
        print("[FAKE] Conveyer started successfully")
        return True
    
    def conveyer_stop(self) -> bool:
        """
        Stop motor to the conveyer
            Returns:
                bool: True if operation is completed, False if failed
        
        """
        print("[FAKE] Conveyer stopped successfully")
        return True

    def engage(self):
        """
        Engage motor to the robot ARM
            Returns:
                bool: True if operation is completed, False if failed
        
        """
        print("[FAKE] Robot is Engaged")
        return True

    def disengage(self):
        """
        Disengage motor to the robot ARM
            Returns:
                bool: True if operation is completed, False if failed
        
        """
        print("[FAKE] Robot is Disengaged")
        return True

    def manualCartMode(self):
        """
        Set manual cartesian mode for robot ARM.
            Returns:
                bool: True if operation is completed, False if failed
        
        """
        self.cart_mode = True
        self.joint_mode = False
        print("[FAKE] Cartesian mode activated")
        return True

    def manualJointMode(self):
        """
        Set manual joint mode for robot ARM.
            Returns:
                bool: True if operation is completed, False if failed
        
        """
        self.joint_mode = True
        self.cart_mode = False
        print("[FAKE] Joint mode activated")
        return True

    def setJointVelocity(self, velocity):
        """
        Robot ARM control in joint mode by joysticks.
            Args:
                velocity(list(double)): joint velocity (motor1, motor2, motor3, motor4, motor5, motor6)

            Returns:
                bool: True if operation is completed, False if failed
        
        """
        if self.joint_mode:
            print(f"[FAKE] Суставная скорость установлена: {velocity}") #???????????
            return True
        else:
            print("Actual robot state isn't joint mode")
            return False

    
    def setLinearTrackVelocity(self, velocity=None) -> bool:
        """
        Robot Linear Track control in joint mode by joysticks.
            Args:
                velocity(list(double)): joint velocity
            Returns:
                bool: True if operation is completed, False if failed
        """
        if self.joint_mode:
            print(f"[FAKE] Суставная скорость установлена: {velocity}") #?????????????????????
            return True
        else:
            print("Actual robot state isn't joint mode")
            return False
        

    def setCartesianVelocity(self, velocity):
        """
        Robot ARM control in cartesian mode by joysticks.
            Args:
                velocity(list(double)): cartesian velocity (x, y, z, rx, ry, rz)

            Returns:
                bool: True if operation is completed, False if failed
        
        """
        if self.cart_mode:
            print(f'[FAKE] Линейная скорость установлена: {velocity}')
            return True
        else:        
            print("[FAKE] Actual robot state isn't cartesian mode")
            return False
        

    def moveToStart(self):
        """
        Automatic activate move to start robot ARM.
            Description:
                Used for the button
        """
        print("[FAKE] Robot is at the start position")
        return True
    
    def activateMoveToStart(self) -> bool:
        """
        Manual activate move to start robot ARM.
            Description:
                Used for the hold button
        
        """
        print("[FAKE] Robot move to start")
        return True
    
    def addMoveToPointL(self, waypoint_list, velocity=0.1, acceleration=0.2,
                 rotational_velocity=3.18, rotational_acceleration=6.37,
                 ref_joint_coord_rad=[]) -> bool:
        """
        Adds a MoveL(Linear move) command to the program
        Args:
            waypoint_list(list(WayPoint)): a list of waypoints
            velocity(double): maximum velocity, m/sec
            acceleration(double): maximum acceleration, m/sec^2
            rotational_velocity(double): maximum joint velocity, rad/sec
            rotational_acceleration(double): maximum joint acceleration, rad/sec^2
            ref_joint_coord_rad: reference joint coordinates for the first waypoint
        Description:
            Waypoint([x, y, z, rx, ry, rz]) - the waypoint is set as the absolute position of the manipulator in meters
        Returns:
            bool: True if operation is completed, False if failed
        """
        print('[FAKE] Точка pointL добавлена в программу')
        return True
    
    def addMoveToPointJ(self, waypoint_list=None, rotational_velocity=pi/1.5, rotational_acceleration=(pi/1.5)*2) -> bool:
        """
        Adds MoveJ(Joint move) command to the program
        Args:
            waypoint_list(list(WayPoint)): a list of waypoints
            rotational_velocity(double): maximum joint velocity, rad/sec
            rotational_acceleration(double): maximum joint acceleration, rad/sec^2
        Description:
            Waypoint(0.0, 0.0, 1.57, 0.0, 1.57, 0.0) - the waypoint is set as the position of the motors in radians
        Returns:
            bool: True if operation is completed, False if failed

        """
        print('[FAKE] Точка pointJ добавлена в программу')
        return True
    
    def addLinearTrackMove(self, position: float = 0.0) -> bool:
        """
        Adding LinearTrack movement to an executable program
            Arg: 
                position(int): the position is set in meters 
            Returns:
                bool: True if operation is completed, False if failed
        """
        print('[FAKE] Точка LinearTrack добавлена в программу')
        return True
    
    def addToolState(self, value: int = 0) -> bool:
        """
        Adding Tool state to an executable program
            Arg: 
                value(int): set as 1/0
            Description: 
                When the **value** is 1, the tool will start working
                When the **value** is 0, the tool will stop working
            Returns:
                bool: True if operation is completed, False if failed
        """
        print('[FAKE] Точка ToolState добавлена в программу')
        return True
    
    
    def addWait(self, wait_time: float = 0.0) -> bool:
        """
        Adding wait to an executable program
            Arg: 
                time(float): the time is set in seconds
            Returns:
                bool: True if operation is completed, False if failed
        """
        print('[FAKE] Wait добавлен в программу')
        return True
    
    def addConveyerState(self, value: int = 0) -> bool:
        """
        Adding pipeline state to an executable program
            Arg: 
                value(int): set as 1/0
            Description: 
                When the **value** is 1, the pipeline will start working
                When the **value** is 0, the pipeline will stop working
            Returns:
                bool: True if operation is completed, False if failed
        """
        print('[FAKE] ConveyorState добавлен в программу')
        return True

    def play(self) -> bool:
        """
        Is used for start executable programm
            Returns:
                bool: True if operation is completed, False if failed
        """
        print("[FAKE] Программа запущена")
        return True

    def pause(self)-> bool:
        """
        Is used for pause executable programm
            Returns:
                bool: True if operation is completed, False if failed
        """
        print("[FAKE] Программа на паузе")
        return True

    def stop(self) -> bool:
        """
        Is used for stop executable programm
            Returns:
                bool: True if operation is completed, False if failed
        """
        print("[FAKE] Программа остановлена")
        return True

    def reset(self) -> bool:
        """
        Is used for reset executable programm
            Returns:
                bool: True if operation is completed, False if failed
        """
        print("[FAKE] Программа сброшена")
        return True

    def toolON(self) -> bool:
        """
        Turns on the working tool
            Description:
                If there is a vacuum system, the suction cup is activated.
                In the presence of a gripping device, the grip is compressed.
            Returns:
                bool: True if operation is completed, False if failed
        """
        self.tool_on = True
        print("[FAKE] Инструмент включён")
        return True

    def toolOFF(self) -> bool:
        """
        Turns off the working tool
            Description:
                If there is a vacuum system, the suction cup is disactivated.
                In the presence of a gripping device, the grip is unclenches.
            Returns:
                bool: True if operation is completed, False if failed
        """
        self.tool_on = False
        print("[FAKE] Инструмент выключен")
        return True

    def getRobotMode(self):
        """
        Returns:
            int: actual robot mode or None if failed

        """
        return "JOINT_MODE" if self.joint_mode else "CARTESIAN_MODE" if self.cart_mode else "UNKNOWN"

    def getRobotState(self):
        """
        Returns:
            int: actual robot state or None if failed

        """
        return "CONNECTED" if self.connected else "DISCONNECTED"

    def getActualStateOut(self):
        """
        Returns:
            int: actual state of the interpreter or None if failed

        """
        return "PROGRAM_READY"

    def getMotorPositionTick(self):
        """
        Returns:
            list(float): actual encoder positions or None if failed
        """
        print("[FAKE] Возврат текущей позиции моторов в тиках")
        return [int(p * 1000) for p in self.position]

    def getToolPosition(self):
        """
        Returns:
            list(float): actual tool positions or None if failed
        """
        print("[FAKE] Возврат текущей позиции инструмента")
        return self.position

    def getMotorPositionRadians(self):
        """
        Returns:
            list(float): actual motor positions in radians or None if failed
        """
        print("[FAKE] Возврат текущей позиции моторов в радианах")
        return self.position
    
    def getToolState(self) -> int:
        """
        Returns:
            int: actual tool positions or None if failed
        """
        return 1 if self.tool_on else 0
    
    def getLinearTrackPosition(self) -> float:
        """
        Returns:
            float: actual linear track position or None if failed
        """
        return random.uniform(-1.0, 1.0)

    def getManipulability(self):
        """
        Description:
            Ability to maneuver range 0..1
            0 - critical situation
            1 - safe situation
        
        Returns:
            float: actual manipulability or None if failed
        """
        value = round(random.uniform(0.3, 1.0), 2)
        print(f"[FAKE] Манипулируемость: {value}")
        return value

    def getActualTemperature(self):
        """
        Returns:
            list(float): actual motor temperatures or None if failed
        """
        temp = round(random.uniform(30.0, 60.0), 1)
        print(f"[FAKE] Температура моторов: {temp} °C")
        return temp

    def getToolState(self):
        return self.tool_on

    def moveToInitialPose(self):
        return True

class Conveyer():
    def __init__(self):
        self.status = False
    
    
    def start(self) -> bool:
        if not self.status:
            print('[FAKE] Conveyor is started')
            self.status = True
            return True
        else:
            print('[FAKE] Failed to start conveyor')
            return False
        
        
    def start(self) -> bool:
        if self.status:
            print('Conveyor is stopped')
            self.status = False
            return True
        else:
            print('[FAKE] Failed to stop conveyor')
            return False