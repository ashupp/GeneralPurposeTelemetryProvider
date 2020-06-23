import gremlin
import socket
from gremlin.user_plugin import *

gremlin.util.log("started sfx100 input 0.0.2.0c")

mode = ModeVariable(
    "Mode",
    "The mode to use for this mapping"
)

axis_X = PhysicalInputVariable(
    "Axis X Roll (Left / Right)",
    "Axis X",
    [gremlin.common.InputType.JoystickAxis]
)

axis_Y = PhysicalInputVariable(
    "Axis Y Pitch (Up / Down)",
    "Axis Y",
    [gremlin.common.InputType.JoystickAxis]
)

axis_ZS = PhysicalInputVariable(
    "Axis Z Surge (Forward / Backward)",
    "Axis Z",
    [gremlin.common.InputType.JoystickAxis]
)

axis_ZR = PhysicalInputVariable(
    "Axis Z Yaw (Rotation of the Stick)",
    "Axis Z Yaw",
    [gremlin.common.InputType.JoystickAxis]
)

axis_SL = PhysicalInputVariable(
    "Slider Heave",
    "Slider",
    [gremlin.common.InputType.JoystickAxis]
)

decorator_X = axis_X.create_decorator(mode.value)
decorator_Y = axis_Y.create_decorator(mode.value)
decorator_ZS = axis_ZS.create_decorator(mode.value)
decorator_ZR = axis_ZR.create_decorator(mode.value)
decorator_SL = axis_SL.create_decorator(mode.value)

heave = 0
roll = 0
pitch = 0
surge = 0
yaw = 0
timerIsActive = 0

opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

@gremlin.input_devices.periodic(0.016)
def update_cycle():
    send_data()


@decorator_X.axis(axis_X.input_id)
def axis_X_evt(event):
    global roll
    roll = event.value
    pass


@decorator_Y.axis(axis_Y.input_id)
def axis_Y_evt(event):
    global pitch
    pitch = event.value
    pass


@decorator_ZS.axis(axis_ZS.input_id)
def axis_ZS_evt(event):
    global surge
    surge = event.value
    pass


@decorator_ZR.axis(axis_ZR.input_id)
def axis_ZR_evt(event):
    global yaw
    yaw = event.value
    pass


@decorator_SL.axis(axis_SL.input_id)
def axis_SL_evt(event):
    global heave
    heave = event.value
    pass


def send_data():
    global timerIsActive
    byte_message = bytes("pitch=" + str(pitch * 100) + "\r\n"
                         + "roll=" + str(roll * 100) + "\r\n"
                         + "surge=" + str(surge * 100) + "\r\n"
                         + "yaw=" + str(yaw * 100) + "\r\n"
                         + "heave=" + str(heave * 100) + "\r\n"
                         , "utf-8")
    opened_socket.sendto(byte_message, ("127.0.0.1", 26999))


send_data()
update_cycle()
