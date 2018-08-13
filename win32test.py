import win32gui

def main():
    window = win32gui.FindWindow(None, 'Sega Mega Drive Classics')

    left, top, right, bottom = win32gui.GetWindowRect(window)
    print(f'left: {left}')
    print(f'top: {top}')
    print(f'right: {right}')
    print(f'bottom: {bottom}')


if __name__ == '__main__':
    main()
