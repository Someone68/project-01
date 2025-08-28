import os
import time
import glob

from pprint import pprint
from import_utils import in_venv
import install_packages
from game import *

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



################
# INTERACTIONS #
################

#Interaction.play_file("interactions/teacher_first.json", NPC, player)
#Interaction.play_file("interactions/fjock.json", NPC, player)
#Interaction.play_file("interactions/ferd.json", NPC, player)



# def first_interaction():
#   tprint("Who do you want to talk to?", "light_yellow")
#   options = [names["ms_finessa"], names["fjock"], names["ferd"], names["fopular_girl"], "Awkardly walk away"]
#   talkto = select_menu(options)

#   if (talkto == 4):
#     dialogue(f"* {player.name} never made any friends.")
#     player.popularity = -20
#     player.karma = 0
#     dialogue(f"* {player.name} went to bed at night, contemplating their life choices.")
#     dialogue(f"* {player.name} eventually moved out of their parent's home...")
#     dialogue(f"* and went to community follege.")
#     dialogue(f"* They soon lost their job, and spent their time reading...")
#     dialogue(f"* and watching the seafood cooking channel...")
#     cprint(draw_box("YOU LOSE\nBAD ENDING", height=4), "red")
#   else:
#     cls_fancy()
#     person = options[talkto].upper()
#     global in_interaction, interaction_with
#     in_interaction = True
#     interaction_with = person
#     tprint(f"-- Interaction with {person} ---------", spd=0.01, clr="light_green")

#     match talkto:
#       case 0:
#         NPC.ms_finessa.talk(f"* Oh hello! A new student! I'm Ms. Finessa, your teacher.")
#         names["ms_finessa"] = "Ms. Finessa"
#         interaction_with = names["ms_finessa"]
#         dialogue(f"* You introduce yourself to Ms. Finessa.")
#         NPC.ms_finessa.talk(f"* Is there something that you need?", title=names["ms_finessa"], color="light_yellow")
#         print()
#         options1 = ["Tell her you don't want to be here", "Call her \"Mom\"", "\"I love school already!\"", "Flirt", "Leave awkwardly"]
#         while (len(options1) > 1):
#           match select_menu(options1):
#             case 0:
#               cls_fancy()
#               dialogue("* Oh, I'm sorry to hear that! I'm sure school is quite overwhelming.", title=names["ms_finessa"], color="light_yellow")
#               dialogue("* You might not love it at first, but I hope you will learn to enjoy it!", title=names["ms_finessa"], color="light_yellow")
#               player.karma -= 10
#               dialogue("* You feel embarrassed and leave.\n-10 KARMA", color="red")
#               options1 = []
#               cls_fancy()
#             case 1:
#               cls_fancy()
#               dialogue("* Oh, you must still think you're at home!", title=names["ms_finessa"], color="light_yellow")
#               dialogue("* I'm sorry, but we are at school, and I am not your mom.", title=names["ms_finessa"], color="light_yellow")
#               player.karma -= 5
#               options1.remove("Call her \"Mom\"")
#               cls_fancy()
#             case 2:
#               cls_fancy()
#               dialogue("* That's wonderful! It's great that you are enjoying your time here!", title=names["ms_finessa"], color="light_yellow")
#               dialogue("* Make sure you save some of that energy for my class!", title=names["ms_finessa"], color="light_yellow")
#               player.karma += 5
#               options2 = ["Ask her about your day", "Ask her about her hobbies", "Bye"]
#               while (len(options2) > 1):
#                 match select_menu(options2):
#                   case 0:
#                     cls_fancy()
#                     dialogue("* My day? It's wonderful! I got to meet so many new students, like you!", title=names["ms_finessa"], color="light_yellow")
#                   case 1:
#                     cls_fancy()
#                     dialogue("* In my free time, I love to read books and play chess. What about you?")
#                     match select_menu(["Dumpster diving", "Playing sports", "Eating food", "Reading", "Working out"]):
#                       case 0:
#                         pass
#             case _:
#               break
# fish goes on a jounrey

# ┛┗┌┐┘└│─┏┓┃━
