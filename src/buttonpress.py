
import keyboard
import time
# -----------------------------------------------------------------------------------
#   This file contains the basic action each entity can preform during it attempts at
# Sonic 3 and Knuckles.
# -----------------------------------------------------------------------------------
def general_action(action, delay):

    if action == '':
        time.sleep(delay)
    else:
        keyboard.press(action)
        time.sleep(delay)
        keyboard.release(action)

def spindash(action, delay):

    keyboard.press(action[0])
    time.sleep(delay)

    for x in range(0, 3):
        keyboard.press(action[1])
        time.sleep(0.3)
        keyboard.release(action[1])
        time.sleep(0.1)

    keyboard.release(action[0])

def jump_shield(action, delay):

    keyboard.press(action[0])
    time.sleep(0.5)
    keyboard.release(action[0])
    time.sleep(0.01)
    keyboard.press(action[1])
    time.sleep(delay)
    keyboard.release(action[1])

def jump_left_or_right(action, delay):

    keyboard.press(action[0])
    time.sleep(1)
    keyboard.press(action[1])
    time.sleep(delay)
    keyboard.release(action[1])
    keyboard.release(action[0])

def save_state():
    keyboard.press('R')
    time.sleep(3)
    keyboard.release('R')

def load_state():
    keyboard.press('T')
    time.sleep(3)
    keyboard.release('T')
