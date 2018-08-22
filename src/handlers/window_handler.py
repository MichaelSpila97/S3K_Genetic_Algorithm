import threading
import time
import os
import win32gui
import win32con

win_hwnd = None
win_pos = []
orig_win_pos = []

def setup_game():
        global win_hwnd, win_pos, orig_win_pos

        # Stores Current directory so it can return to it after launching game
        current_dir = os.getcwd()

        # Goes to games directory and lauches its .exe in a thread
        os.chdir("E:\Steam\steamapps\common\Sega Classics")
        gamethread = threading.Thread(target=lambda: os.system("SEGAGameRoom.exe"), daemon=True)
        gamethread.start()

        # Wait Five seconds to give game time to launch before obtaining window handler
        # and setting the window to the top right corner of the screen
        time.sleep(5)
        win_hwnd = win32gui.FindWindow(None, 'SEGA Mega Drive Classics')
        win32gui.SetWindowPos(win_hwnd, win32con.HWND_TOPMOST, 0, 0, 646, 509, 0)

        left, top, right, bottom = win32gui.GetWindowRect(win_hwnd)
        orig_win_pos = [left, top, right, bottom]
        curr_win_pos = [left, top, right, bottom]

        # Returns to original directory so the program can save and load entity data
        # properly
        os.chdir(current_dir)

        window_thread = threading.Thread(target=update_window_pos, daemon=True)
        window_thread.start()

def update_window_pos():
    global win_pos
    while True:
        left, top, right, bottom = win32gui.GetWindowRect(win_hwnd)
        updated_pos = [left, top, right, bottom]

        if updated_pos != win_pos:
            print(f'\nupdated_pos: {updated_pos}\ncur_win_pos: {win_pos}\n')
            win_pos = [left, top, right, bottom]
