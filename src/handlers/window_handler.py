import threading
import time
import os
import win32gui
import win32con

# Globals keeps that keeps tracks of basic info on the game window
win_hwnd = None
win_pos = []
orig_win_pos = []

exe_location = "E:\Steam\steamapps\common\Sega Classics"
# Fuction that executes and setups the inital postion of the game window on the screen
def setup_game():
        global win_hwnd, win_pos, orig_win_pos

        # Stores Current directory so it can return to it after launching game
        current_dir = os.getcwd()

        # Goes to games directory and lauches its .exe in a thread
        os.chdir(exe_location)
        gamethread = threading.Thread(target=lambda: os.system("SEGAGameRoom.exe"), daemon=True)
        gamethread.start()

        # Wait Five seconds to give game time to launch before obtaining window handler
        # and setting the window to the top right corner of the screen
        time.sleep(5)
        win_hwnd = win32gui.FindWindow(None, 'SEGA Mega Drive Classics')
        win32gui.SetWindowPos(win_hwnd, win32con.HWND_TOPMOST, 0, 0, 646, 509, 0)

        # Obtains starting window position values and sets them to orig_win_pos
        # and win_pos.
        #
        # Win_pos and orig_win_pos will be used to reajdust  the screen
        # reader if the window moves
        left, top, right, bottom = win32gui.GetWindowRect(win_hwnd)
        orig_win_pos = [left, top, right, bottom]
        win_pos = [left, top, right, bottom]

        # Returns to original directory so the program can save and load entity data
        # properly
        os.chdir(current_dir)

        # Lauches thread that keeps tracks of the games window position
        window_thread = threading.Thread(target=update_window_pos, daemon=True)
        window_thread.start()

# Function that keeps tracks of windows postion through constant polling
# Updates win_pos if win_pos does not equal the updated_pos that was just read in
def update_window_pos():
    global win_pos
    while True:
        left, top, right, bottom = win32gui.GetWindowRect(win_hwnd)
        updated_pos = [left, top, right, bottom]

        if updated_pos != win_pos:
            print(f'\nupdated_pos: {updated_pos}\ncur_win_pos: {win_pos}\n')
            win_pos = [left, top, right, bottom]


# Function calcuates the x and y padding of the game window if it is moved from
# its original postion
#
# Returns the x and y pad if window is moved from original pos
# Else returns 0, 0 if the window is still in its original postion
def adjust_box():
    if win_pos != orig_win_pos:
        x_pad = win_pos[0] - orig_win_pos[0]
        y_pad = win_pos[1] - orig_win_pos[1]

        return x_pad, y_pad
    return 0, 0
