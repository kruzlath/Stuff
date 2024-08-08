from kscript import *
import os
import json
import win32api
import win32con
import win32gui
import ctypes
import pyautogui
from ctypes import wintypes
from pynput.mouse import Listener
import _thread

from Scripts.Stuffdef import *

#Screen Setup
transparent = (4,232,12)
clock=pygame.time.Clock()
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparent), 0, win32con.LWA_COLORKEY)
user32 = ctypes.WinDLL("user32")
user32.SetWindowPos.restype = wintypes.HWND
user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.UINT]
user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001)

#Mouse Handler
size_offset=[(1800-i[0]*900)/i[1] for i in enumerate(pyautogui.size())]
ctimer=[0 for i in range(3)]
dctimer=[0 for i in range(3)]
click=[False for i in range(3)]
def on_click(*args):
    # see what argument is passed.
    if args[-1]:
        if args[2].name=="left":
            dctimer[0]=1
        if args[2].name=="right":
            dctimer[2]=1
        
        # Do something when the mouse key is pressed.
        

    elif not args[-1]:
        if args[2].name=="left":
            dctimer[0]=0
            ctimer[0]=0
        if args[2].name=="right":
            dctimer[2]=0
            ctimer[2]=0
        # Do something when the mouse key is released.
        pass
def s_threat_paralel_1():
    # Open Listener for mouse key presses
    with Listener(on_click=on_click) as listener:
        # Listen to the mouse key presses
        listener.join()
_thread.start_new_thread(s_threat_paralel_1)



menu="None"


#Mainloop
while run:
    ctimer=[ctimer[i]+dctimer[i] for i in range(3)]
    click=[ctimer[i]==1 for i in range(3)]
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        elif event.type==pygame.MOUSEWHEEL:
            mouse_scroll=event.y
    mouse_pos=[size_offset[i[0]]*i[1] for i in enumerate(pyautogui.position())]
    win.fill(transparent)
    if menu=="None":
       # print(mouse_pos)
        dist_from_button=dist(mouse_pos,(900,0))
        if dist_from_button<30:
            pygame.draw.circle(win,(255,255,255),(900,0),10,3)
        if dist_from_button<10:
            menu="Open Navigation"
    elif menu=="Open Navigation":
        if Submit_Button.display(win,70,30,mouse_pos,click): menu="Submit"
        if M_Button.display(win,240,30,mouse_pos,click): menu="Choose M"
        pygame.draw.circle(win,(255,255,255),(900,100),10,3)
        if dist(mouse_pos,(900,100))<10:    menu="None"
    elif menu=="Submit":
        if E_button.display(win,70,30,mouse_pos,click): pass
    endframe()
pygame.quit()