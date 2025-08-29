import os
import time
import glob

from pprint import pprint
from import_utils import in_venv
import install_packages
from game import *

"""
Hi guy who checks my code! You are free to look around of course, just that the code is really messy. If you will, I'll explain how stuff works here. Very little dialogue is actually in the main file. They are played through INTERACTIONS. You can find a bunch of them in the file path ./interactions! They all contain dialogue and are completely modular! So you can change the files and when you run the program it will reflect those changes! If you want to "mod" this game add new interactions, just make a new file in the interactions folder! You can set the variable DEV_MODE to True so that you can play the interaction if you want to test it. Interaction format is kind of weird, so just look around at other interactions to copy. To actually play the interactions in-game, you can use DEV MODE or add them somewhere. Have fun!
"""


if (not in_venv()):
  print("This program uses external libraries that will be automatically installed. A virtual environment (venv) will be created in this folder, and packages will be installed! The program will then restart! This is because global Python package installations are becoming deprecated, and is even completely unsupported on Arch Linux! Some IDEs may NOT support this! You can run this in your command prompt / terminal if it doesn't work!")
  print("Make sure that you are using Python 3.12 or newer! Otherwise, this might not work! If you are using a pre-packaged Python processor, like on Thonny, Python 3.12 might not be supported!")
  input ("[PRESS ENTER TO CONTINUE]\n")
else:
  print("For the best experience, please use Python 3.12 or newer! This game runs in your terminal, so please resize it so that it is large! It is NOT recommended to 'scroll' through your terminal. Things may break. Keep in mind that on Linux, if it doesn't work, try re-running the program with root (sudo python main.py).")
  input("[PRESS ENTER TO CONTINUE]\n")

install_packages.init()

from game import *
from termcolor import colored, cprint
import cursor
import cutie
from npcs import *

in_interaction = False
interaction_with = ""

DEV_MODE = True

if (DEV_MODE):
  if (input("YOU ARE IN DEVELOPER MODE!\nThis mode is only for debugging purposes!\nPress enter if you want to continue in developer mode!\nTo return to \"verified\" mode, type 'v' and press enter! \n INIT> ").lower() == "v"):
    DEV_MODE = False
  else:
    print("continuing in developer mode, have fun!")
    sleep(3)
  
  cls()
  

dialogue("Somewhere in the mystical land of fishtopia...", color="magenta")

cls()

cprint("""
      _\\_
   \\/  o \\
   //\\___=
      ''
      """, "light_blue")

dialogue("* glub glub", title="???")

cls()

def set_name():
    namesel = tinput("* What is your name? (min 3 chars, max 7, no spaces) ", "light_yellow")

    while (len(namesel.strip()) < 3 or len(namesel.strip()) > 7 or ' ' in namesel): # check if input is invalid
        cls()
        cprint("invalid name", "red") # i had to write these comments because decaf cant read code
        namesel = input(colored("* What is your name? (min 3 chars, max 7, no spaces) ", "light_yellow"))

    return namesel



player.set_name(set_name().strip())

if (DEV_MODE): dev_mode()

dialogue(f"* After waking up and doing their daily routines...")

dialogue(f"{player.name} swims to Fishtopia Elementary.")

dialogue(f"* It's {player.name}'s first day at school.")

dialogue(f"* But {player.name} isn't that popular. Let's go help them make friends!")

dialogue(f"* After stumbling around in the halls...")

Interaction.play_file("./interactions/init.json")