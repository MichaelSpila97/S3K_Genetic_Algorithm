
import keyboard
import time

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

def start_next_game():

    # Presses enter to move to save select screen
    time.sleep(5)
    keyboard.press('enter')
    time.sleep(0.1)
    keyboard.release('enter')

    time.sleep(5)

    # Press left to move cursor over the no save selection
    keyboard.press('left')
    time.sleep(0.1)
    keyboard.release('left')

    time.sleep(1)

    # Press enter to start the game
    keyboard.press('enter')
    time.sleep(0.2)
    keyboard.release('enter')

def save_state():
    keyboard.press('F2')
    time.sleep(3)
    keyboard.release('F2')

def load_state():
    keyboard.press('F3')
    time.sleep(3)
    keyboard.release('F3')
