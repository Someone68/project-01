import time
import install_packages

install_packages.init()

from utils import tprint, tinput, select_menu, draw_box, dialogue
from termcolor import colored, cprint
import cutie

print(draw_box("Skibidi game", title="title"))

cprint("""
~~ random shit ~~
    """, "light_red")

option = select_menu(["SKIBIDI MENU", "OPTION 1: SKIBIDI", "OPTION 2: SIGMA", "OPTION 3: OHIO", "GYATT MENU", "OPTION 4: FORTNIET", "OPTION 5: TSPMO"], [0, 4], sel_index=1)

if (option >= 1 and option <= 3): dialogue("YOU ARE SKIOBIDI", title="The Rizzler")
else: dialogue("YOU ARE GAYAT", title="The Rizzler")

# ┛┗┌┐┘└│─┏┓┃━
