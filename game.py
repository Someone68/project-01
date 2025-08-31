import random
import sys
import cutie
import cursor
import os
import textwrap
import json
import re
import glob
from pprint import pprint
from time import sleep
import time
import readchar
from termcolor import colored, cprint
from blessed import Terminal
from npcs import register_npcs, INTERNAL_NPC_NAMES
term = Terminal()

class Player:
    def __init__(self, name):
        self.name = name
        self.karma = 50
        self.popularity = 0
        self.interaction_status = False
        self.interaction_with = ""
        self.flags = {}

    def set_name(self, name):
        self.name = name.upper()
        
    def fb_offense_turn(self):
        yds_to_goal = 50
        downs = 4
        
        while (downs > 0 and yds_to_goal > 0):
            cls_fancy()
            print(colored("OFFENSE", "red", attrs=["bold"]) + colored(" SIDE", "cyan"))
            print(colored(f"{downs:{7}}", "red", attrs=["bold"]) + colored(" DOWNS", "cyan"))
            print(colored(f"{yds_to_goal:{7}}", "red", attrs=["bold"]) + colored(" YDS", "cyan"))
            
            gain = 0
            cprint("Choose a play:", "magenta")
            play = select_menu(["Running play", "Passing play"])
            cls_fancy()
            match play:
                case 0:
                    gain = random.randint(-2, 10)
                    sleep(abs(gain // 2))
                    if (gain < 0):
                        cprint(f"TACKLED! | {gain} YDS!", "red")
                        input ("Press enter to continue . . . ")
                    elif (gain > 0):
                        cprint(f"SUCCESS! | +{gain} YDS!", "green")
                        input ("Press enter to continue . . . ")
                    else:
                        cprint(f"TACKLED! | NO GAIN", "red")
                        input ("Press enter to continue . . . ")
                case 1:
                    cprint(f"PASSING PLAY | PRESS KEYS AS THEY APPEAR")
                    sleep(2)
                    cprint("Ready?")
                    sleep(1)
                    cprint("Get set...")
                    sleep(1)
                    cprint("Go!")
                    seq_length = random.randint(3, 5)
                    key_sequence = [random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(seq_length)]
                    max_time_per_key = 1.5  # seconds per key

                    for i, target in enumerate(key_sequence):
                        cprint(f"\nPRESS '{target.upper()}' NOW!", random.choice(["red", "green", "blue", "yellow", "magenta", "cyan"]))
                        start_time = time.time()
                        key = readchar.readchar()
                        reaction = time.time() - start_time
                        
                        gain = random.randint(10, 20)
                        
                        if key.lower() != target:
                            cprint(f"INTERCEPTED! DEFENSE TAKES OVER!")
                            return 0
                        elif reaction > max_time_per_key:
                            cprint(f"TOO SLOW! DEFENSE TAKES OVER!")
                            return 0
                        else:
                            cprint(f"SUCCESS! +{gain} YDS!")
                    
            yds_to_goal -= gain
            if (yds_to_goal <= 0):
                cprint("TOUCHDOWN! | SCORED 7 PTS!", "cyan")
                NPC.get("Fjock").talk(random.choice(["Damn! Nice job team!", "Let's go!!!", "Nice touchdown!"]))
                cls_fancy()
                return 7

            if (gain <= 0):
                cprint("NO PROGRESS ON PLAY!", "red")
            
            downs -= 1
            time.sleep(1)

        cprint("FAILED TO SCORE! NO POINTS GAINED!", "red")
        
        NPC.get("Fjock").talk(random.choice(["Damn, we'll get 'em next time.", "Damn it! We didn't get to score!"]))
        cls_fancy()
    
    def football_minigame(self): # hell yeah
        cprint("Ready?", "red")
        match select_menu(["Let's Rock!", "how to play football!1?!!"]):
            case 1:
                cls_fancy()
                NPC.get("Nass").talk("...You don't know how to play football?")
                cls_fancy()
                NPC.get("Nass").talk("I have a feeling that you failed your PE class.")
                cls_fancy()
                NPC.get("Nass").talk("...Fine. I'll tell you how to play.")
                cls_fancy()
                NPC.get("Nass").talk("There are two sides, attack and defense.")
                cls_fancy()
                NPC.get("Nass").talk("On the attacking side...")
                cls_fancy()
                NPC.get("Nass").talk("Kick the ball, pass, and run toward the opponent's goal.")
                cls_fancy()
                NPC.get("Nass").talk("Score by getting the ball into their net.")
                cls_fancy()
                NPC.get("Nass").talk("On the defense side...")
                cls_fancy()
                NPC.get("Nass").talk("Defend your own goal from their attacks")
                cls_fancy()
                NPC.get("Nass").talk("More goals = win.")
                cls_fancy()
                NPC.get("Nass").talk("On offense, you have 4 downs (tries) to make a goal.")
                cls_fancy()
                NPC.get("Nass").talk("Good luck, stupid.")
                cls_fancy()
        
        print(self.fb_offense_turn())
        input()
        

player = Player("error")

class Npc:
  def __init__(self, name, defname = None, color = "white"):
    self.name = name
    if (not defname): self.defname = name
    else: self.defname = defname
    self.memory = { "name_unlocked" : False }
    self.color = color

  def unlock_name(self):
    self.memory["name_unlocked"] = True

  def get_name(self):
    return self.name if self.memory["name_unlocked"] else self.defname

  def talk(self, text, wait_for_input = True):
    width=30
    height=5
    h_align="left"
    v_align="top"
    padding=1
    title=self.name if self.memory["name_unlocked"] else self.defname
    color=self.color
    speed=0.01
    cursor.hide()

    if (self.name in INTERNAL_NPC_NAMES):
        title = None

    def tprint_line(line, row, col):
      sys.stdout.write(f"\033[{row};{col}H")  # move to row, col
      for char in line:
          print(colored(char, color) if color else char, end='', flush=True)
          sleep(speed * 7 if char == '.' or char == '!' or char == '?' else speed * 5 if char == ',' else speed)
      print("\033[0m", end='', flush=True)  # reset color

    if isinstance(text, str):
      text_lines = text.splitlines()
    else:
      text_lines = list(text)

    usable_width = width - 2 - 2 * padding
    wrapped_lines = []
    for line in text_lines:
      wrapped_lines.extend(textwrap.wrap(line, width=usable_width))

    def align_line(line):
      if h_align == "left":
        return line.ljust(usable_width)
      elif h_align == "center":
        return line.center(usable_width)
      elif h_align == "right":
        return line.rjust(usable_width)
      else:
        raise ValueError("Invalid h_align")

    aligned_lines = [(" " * padding) + align_line(line) + (" " * padding) for line in wrapped_lines]

    # Top border
    if title:
        title_str = f"━ {title} ━"
        title_len = len(title_str)
        remaining_len = width - 2 - title_len
        if remaining_len < 0:
            raise ValueError("Title too long for box width.")
        top = "┏" + title_str + "━" * remaining_len + "┓"
    else:
        top = "┏" + "━" * (width - 2) + "┓"
    bottom = "┗" + "━" * (width - 2) + "┛"

    empty_line = " " * (width - 2)
    num_content_lines = len(aligned_lines)
    blank_lines = height - 2 - num_content_lines
    if blank_lines < 0:
        raise ValueError("Not enough vertical space for wrapped content.")

    if v_align == "top":
        top_pad = 0
    elif v_align == "center":
        top_pad = blank_lines // 2
    elif v_align == "bottom":
        top_pad = blank_lines
    else:
        raise ValueError("Invalid v_align")

    bottom_pad = blank_lines - top_pad

    # Build the box lines
    box_lines = [top]
    for _ in range(top_pad):
        box_lines.append("┃" + empty_line + "┃")
    for _ in aligned_lines:
        box_lines.append("┃" + " " * (width - 2) + "┃")
    for _ in range(bottom_pad):
        box_lines.append("┃" + empty_line + "┃")
    box_lines.append(bottom)

    # Get current terminal row
    with term.location():
        start_row = term.get_location()[0]

    # Print the full box at current cursor location
    for line in box_lines:
        print(line)

    # Type each line at the right spot
    for i, line in enumerate(aligned_lines):
        row = start_row + 2 + top_pad + i
        col = 2
        tprint_line(line, row, col)
    
    # Calculate where the arrow really goes
    total_box_height = len(box_lines)  # includes top + bottom border
    arrow_row = start_row + total_box_height - 1  # second to last line
    arrow_col = width - 2  # one before right border

    # Place the arrow
    sys.stdout.write(f"\033[{arrow_row};{arrow_col}H")
    print("▼", end='', flush=True)
    
    final_row = start_row + len(box_lines)
    sys.stdout.write(f"\033[{final_row};1H")
    sys.stdout.flush()

    flush_input()

    if (wait_for_input):
        with term.cbreak():
            term.inkey()

    print()
    cursor.show()

class NpcRegistry:
    def __init__(self):
        self._npcs = {}

    def add(self, npc):
        self._npcs[npc.name.lower()] = npc
        setattr(self, npc.name.lower(), npc)

    def get(self, name):
        return self._npcs.get(name.lower())

NPC = NpcRegistry()
register_npcs(NPC)


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def cls_fancy():
    cls()
    if (player):
        cprint(f"KARMA: {player.karma} / 100", "light_red", attrs=["bold"])
        cprint(f"POPULARITY: {player.popularity} / 100", "light_blue", attrs=["bold"])
        print()

def dialogue(text,
    width=30,
    height=5,
    h_align="left",
    v_align="top",
    padding=1,
    title=None,
    color=None,
    speed=0.01):
  show_dialogue(text, width, height, h_align, v_align, padding, title, color, speed)
  cls_fancy()

def tprint(txt, clr=None, spd=0.02):
    for x in txt:
        print(colored(x, no_color=True if clr == None else False, color=clr if clr != None else None), end='')
        sys.stdout.flush()
        sleep(spd)
    print()

def tinput(txt, clr=None, spd=0.02):
    for x in txt:
        print(colored(x, no_color=True if clr == None else False, color=clr if clr != None else None), end='')
        sys.stdout.flush()
        sleep(spd)
    flush_input()
    return input()

def select_menu(options=["you", "forgot", "to put", "the actual", "options", "lmao"], caption_indicies=None, sel_index=0, desel_prefix="   ", sel_prefix=colored(" $ ", "magenta"), capt_prefix=" ", confirm_on_select=True):
    cursor.hide()
    selected = cutie.select(options, caption_indicies, desel_prefix, sel_prefix, capt_prefix, sel_index, confirm_on_select)
    cursor.show()
    return selected

def draw_box(
    text,
    width=30,
    height=5,
    h_align="center",
    v_align="center",
    padding=0,
    title=None
):
    if isinstance(text, str):
        lines = text.splitlines()
    else:
        lines = list(text)

    max_line_len = max(len(line) for line in lines) if lines else 0
    usable_width = width - 2 - 2 * padding
    if usable_width < max_line_len:
        raise ValueError("Text too wide for box with given padding.")

    # Build top border with optional title
    if title:
        title_str = f"━ {title} ━"
        title_len = len(title_str)
        remaining_len = width - 2 - title_len
        if remaining_len < 0:
            raise ValueError("Title too long for box width.")
        top = "┏" + title_str + ("━" * remaining_len) + "┓"
    else:
        top = "┏" + "━" * (width - 2) + "┓"

    bottom = "┗" + "━" * (width - 2) + "┛"

    # Horizontal alignment formatter
    def align_line(line):
        if h_align == "left":
            return line.ljust(usable_width)
        elif h_align == "center":
            return line.center(usable_width)
        elif h_align == "right":
            return line.rjust(usable_width)
        else:
            raise ValueError("Invalid h_align: choose 'left', 'center', or 'right'")

    aligned_lines = [(" " * padding) + align_line(line) + (" " * padding) for line in lines]

    # Vertical alignment
    empty_line = " " * (width - 2)
    num_content_lines = len(aligned_lines)
    blank_lines = height - 2 - num_content_lines

    if blank_lines < 0:
        raise ValueError("Not enough vertical space for content")

    if v_align == "top":
        top_pad = 0
    elif v_align == "center":
        top_pad = blank_lines // 2
    elif v_align == "bottom":
        top_pad = blank_lines
    else:
        raise ValueError("Invalid v_align: choose 'top', 'center', or 'bottom'")

    bottom_pad = blank_lines - top_pad

    content = (
        ["┃" + empty_line + "┃"] * top_pad +
        ["┃" + line + "┃" for line in aligned_lines] +
        ["┃" + empty_line + "┃"] * bottom_pad
    )

    return "\n".join([top] + content + [bottom])


def show_dialogue(
    text,
    width=30,
    height=5,
    h_align="left",
    v_align="top",
    padding=1,
    title=None,
    color=None,
    speed=0.01,
    wait_for_input=True,
):
    cursor.hide()

    def tprint_line(line, row, col):
        sys.stdout.write(f"\033[{row};{col}H")  # move to row, col
        for char in line:
            print(colored(char, color) if color else char, end='', flush=True)
            sleep(speed * 7 if char == '.' or char == '!' or char == '?' else speed * 5 if char == ',' else speed)
        print("\033[0m", end='', flush=True)  # reset color

    if isinstance(text, str):
        text_lines = text.splitlines()
    else:
        text_lines = list(text)

    usable_width = width - 2 - 2 * padding
    wrapped_lines = []
    for line in text_lines:
        wrapped_lines.extend(textwrap.wrap(line, width=usable_width))

    def align_line(line):
        if h_align == "left":
            return line.ljust(usable_width)
        elif h_align == "center":
            return line.center(usable_width)
        elif h_align == "right":
            return line.rjust(usable_width)
        else:
            raise ValueError("Invalid h_align")

    aligned_lines = [(" " * padding) + align_line(line) + (" " * padding) for line in wrapped_lines]

    # Top border
    if title:
        title_str = f"━ {title} ━"
        title_len = len(title_str)
        remaining_len = width - 2 - title_len
        if remaining_len < 0:
            raise ValueError("Title too long for box width.")
        top = "┏" + title_str + "━" * remaining_len + "┓"
    else:
        top = "┏" + "━" * (width - 2) + "┓"
    bottom = "┗" + "━" * (width - 2) + "┛"

    empty_line = " " * (width - 2)
    num_content_lines = len(aligned_lines)
    blank_lines = height - 2 - num_content_lines
    if blank_lines < 0:
        raise ValueError("Not enough vertical space for wrapped content.")

    if v_align == "top":
        top_pad = 0
    elif v_align == "center":
        top_pad = blank_lines // 2
    elif v_align == "bottom":
        top_pad = blank_lines
    else:
        raise ValueError("Invalid v_align")

    bottom_pad = blank_lines - top_pad

    # Build the box lines
    box_lines = [top]
    for _ in range(top_pad):
        box_lines.append("┃" + empty_line + "┃")
    for _ in aligned_lines:
        box_lines.append("┃" + " " * (width - 2) + "┃")
    for _ in range(bottom_pad):
        box_lines.append("┃" + empty_line + "┃")
    box_lines.append(bottom)

    # Get current terminal row
    with term.location():
        start_row = term.get_location()[0]

    # Print the full box at current cursor location
    for line in box_lines:
        print(line)

    # Type each line at the right spot
    for i, line in enumerate(aligned_lines):
        row = start_row + 2 + top_pad + i
        col = 2
        tprint_line(line, row, col)

    # Calculate where the arrow really goes
    total_box_height = len(box_lines)  # includes top + bottom border
    arrow_row = start_row + total_box_height - 1  # second to last line
    arrow_col = width - 2  # one before right border

    # Place the arrow
    sys.stdout.write(f"\033[{arrow_row};{arrow_col}H")
    print("▼", end='', flush=True)
    
    final_row = start_row + len(box_lines)
    sys.stdout.write(f"\033[{final_row};1H")
    sys.stdout.flush()

    flush_input()

    if (wait_for_input):
        with term.cbreak():
            term.inkey()

    print()
    cursor.show()


def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

class Interaction:
    def __init__(self, filepath, npc_registry, player):
        self.filepath = filepath
        self.npc_registry = npc_registry
        self.player = player
        self.data = None
        self.default_npc = None
        self.menu_context_stack = []

    def load(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        # Store the default NPC object (if exists)
        self.default_npc = self.npc_registry.get(self.data.get("default_npc"))

    def play(self):
        if not self.data:
            raise ValueError("Interaction not loaded. Call load() first.")
        for action in self.data.get("actions", []):
            self.run_action(action)
    
    def format_text(self, text):
        if not isinstance(text, str):
            return text

        def replace_placeholder(match):
            tag = match.group(1)
            if tag == "player":
                return self.player.name
            elif tag.startswith("npc:"):
                npc_name = tag.split(":", 1)[1]
                npc = self.npc_registry.get(npc_name)
                return npc.get_name() if npc else f"[Unknown NPC:{npc_name}]"
            return match.group(0)

        return re.sub(r"\{([^}]+)\}", replace_placeholder, text)

    def check_condition(self, cond):
        ctype = cond["type"]
        if ctype == "memory_check":
            npc = self.npc_registry.get(cond.get("npc")) if cond.get("npc") else self.default_npc
            key = cond["key"]
            expected = cond.get("value", None)
            if expected is None:
                return key in npc.memory
            return npc.memory.get(key) == expected

        elif ctype == "player_flag":
            flag = cond["flag"]
            expected = cond.get("value", None)
            if expected is None:
                return flag in self.player.flags
            if (expected is False):
                if (not flag in self.player.flags):
                    return True
            return self.player.flags.get(flag) == expected

        elif ctype == "boolean":
            context = {
                "player": self.player,
                "npc": self.default_npc,
                "npc_registry": NPC,
                # add other safe globals here if needed
            }
            return bool(eval(cond["condition"], {}, context))

        else:
            raise ValueError(f"Unknown condition type: {ctype}")

    def run_action(self, action):
        action_type = action.get("type")

        def cls_fancy():
          cls()
          cprint(f"KARMA: {self.player.karma} / 100", "light_red", attrs=["bold"])
          cprint(f"POPULARITY: {self.player.popularity} / 100", "light_blue", attrs=["bold"])
          print("")

        if action_type == "talk":
            npc = self.npc_registry.get(action.get("npc")) if action.get("npc") else self.default_npc
            npc.talk(self.format_text(action["text"]), action.get("wait_for_input", True))

        elif action_type == "play_interaction":
            self.play_file("interactions/" + action.get("interaction") + ".json")

        elif action_type == "show_dialogue":
            show_dialogue(
                self.format_text(action["text"]),
                title=self.format_text(action.get("title")),
                color=action.get("color"),
                wait_for_input=action.get("wait_for_input", True)
            )

        elif action_type == "show_text":
            text = self.format_text(action["text"])
            color = action.get("color")
            typeout = action.get("typeout", True)
            if typeout:
                tprint(text, color)
            else:
                cprint(text, color)

        elif action_type == "talk_mult":
            texts = action["lines"]
            npc = self.npc_registry.get(action.get("npc")) if action.get("npc") else self.default_npc

            for text in texts:
                npc.talk(self.format_text(text), action.get("wait_for_input", True))
                cls_fancy()

        elif action_type == "select_menu":
            repeat = action.get("repeat", False)
            options_to_stop = action.get("options_to_stop", 0)
            options = action["options"]
            selected_index = action.get("selected_index", 0)
            stop_finish_code = False
            menu_title = action.get("title")
            menu_color = action.get("color")
            menu_typeout = action.get("typeout", True)

            caption_indices = []
            for opt in options:
                if opt["type"] == "caption":
                    caption_indices.append(options.index(opt))
                    if selected_index == options.index(opt):
                        selected_index += 1

            # Push this menu context onto the stack
            context = {
                "options": options,
                "selected_index": selected_index,
                "caption_indices": caption_indices
            }
            self.menu_context_stack.append(context)

            while True:
                if len(options) <= 0:
                    break

                # Print title if exists
                if menu_title:
                    if menu_typeout:
                        tprint(self.format_text(menu_title), menu_color)
                    else:
                        cprint(self.format_text(menu_title), menu_color)

                option_labels = [self.format_text(opt["name"]) for opt in options]
                idx = select_menu(option_labels, caption_indicies=caption_indices)
                cls_fancy()

                chosen = options[idx]
                self.run_action(chosen["action"])

                if chosen.get("stop_finish_code") is True:
                    stop_finish_code = True
                elif chosen.get("stop_finish_code") is False:
                    stop_finish_code = False

                if chosen.get("one_time", True):
                    options.pop(idx)

                if chosen.get("end_menu", False):
                    break

                if len(options) <= options_to_stop:
                    break

                if not repeat:
                    break

            # Pop menu context when done
            self.menu_context_stack.pop()

            if not stop_finish_code and "finish_action" in action:
                self.run_action(action["finish_action"])


        elif action_type == "multiple":
            for sub in action["actions"]:
                self.run_action(sub)

        elif action_type == "run_code":
            exec(action["code"], globals(), locals())

        elif action_type == "wait_input":
            flush_input()
            if action.get("wait_for_input", True):
                with term.cbreak():
                    term.inkey()


        elif action_type == "change_stats":
            stat = action["stat"]
            op = action["operation"]
            amt = action["amount"]
            current = getattr(self.player, stat, None)
            if current is None:
                raise AttributeError(f"Player has no attribute '{stat}'")

            if op == "add":
                new_val = current + amt
            elif op == "subtract":
                new_val = current - amt
            elif op == "multiply":
                new_val = current * amt
            elif op == "divide":
                new_val = current / amt
            else:
                raise ValueError(f"Unknown operation '{op}'")

            setattr(self.player, stat, new_val)
            print(f"Player {stat} is now {new_val}")


        elif action_type == "set_memory":
            npc = self.npc_registry.get(action.get("npc")) if action.get("npc") else self.default_npc
            for k, v in action["memory"].items():
                if (type(v) == str):
                    if (v.lower() == "true"):
                        v = True
                    elif (v.lower() == "false"):
                        v = False
                npc.memory[k] = v

        elif action_type == "remove_memory":
            npc = self.npc_registry.get(action.get("npc")) if action.get("npc") else self.default_npc
            for k in action["memories"]:
                npc.memory.pop(k, None)

        elif action_type == "set_flag":
            self.player.flags[action["name"]] = action.get("value", True)

        elif action_type == "condition":
            cond = action["condition"]
            if self.check_condition(cond):
                self.run_action(action["action"])

        elif action_type == "change_select_menu_option":
            if not self.menu_context_stack:
                print("No active select menu to modify!")
                return

            # Work with the current (top of stack) menu
            context = self.menu_context_stack[-1]
            options = context["options"]

            # Add new option
            if "add" in action:
                new_opt = action["add"]
                if "index" in action:
                    idx = action["index"]
                    options.insert(idx, new_opt)
                else:
                    options.append(new_opt)

            # Remove by index
            if "remove_index" in action:
                idx = action["remove_index"]
                if 0 <= idx < len(options):
                    options.pop(idx)

            # Remove by name
            if "remove_name" in action:
                name = action["remove_name"]
                options[:] = [opt for opt in options if opt["name"] != name]

            # Modify by index
            if "modify_index" in action:
                idx = action["modify_index"]
                new_data = action.get("new_data", {})
                if 0 <= idx < len(options):
                    options[idx].update(new_data)

        elif action_type == "comment":
            pass

        else:
            raise ValueError(f"Unknown interaction type: {action_type}")

        cls_fancy()

    @staticmethod
    def play_file(filepath, npc_registry=NPC, player=player):
      inter = Interaction(filepath, npc_registry, player)
      inter.load()
      inter.play()

def dev_mode():
    to_continue = False
    cls_fancy()
    cprint("DEVELOPER TOOLS", "yellow")
    cprint("SELECT AN OPTION")
    option = select_menu(["run interaction", "view player object", "edit stats", "football minigame :3", "continue", "quit"])

    cls_fancy()
    cprint("DEVELOPER TOOLS", "yellow")
    match(option):
        case 0:   
            cprint("RUN INTERACTION", "yellow")
            interactions_list = glob.glob("./interactions/*.json")
            interactions_list.append("cancel")
            menu = select_menu(interactions_list)
            if (interactions_list[menu] != "cancel"):
                Interaction.play_file(interactions_list[menu])
            input("interaction finished, press enter to continue...")
        case 1:
            cprint("PLAYER STATS", "yellow")
            pprint(vars(player))
            input("enter to continue...")
        case 2:
            cprint("EDIT STATS", "yellow")
            stat = select_menu(["flags", "karma", "popularity", "name", "cancel"])
            match(stat):
                case 0:   
                    cprint("SET FLAG", "yellow")
                    to_set = input("flag to set: ")
                    set_value = input("flag value (true/false): ")
                    print(set_value.lower() == "true")
                    if (set_value.lower() == "true" or set_value.lower() == "1"):
                        set_value = True
                    elif (set_value.lower() == "false" or set_value.lower() == "0"):
                        set_value = False
                    else:
                        print("input error, using true as default")
                        set_value = True
                    player.flags[to_set] = set_value
                    input("flag set. enter to continue")
                case 1:
                    cprint("SET STAT: KARMA", "yellow")
                    to_set = int(input("set value (int): "))
                    player.karma = to_set
                    input("karma set. enter to continue")
                case 2:
                    cprint("SET STAT: POPULARITY", "yellow")
                    to_set = int(input("set value (int): "))
                    player.popularity = to_set
                    input("popularity set. enter to continue")
                case 3:
                    cprint("SET STAT: NAME", "yellow")
                    to_set = input("set name (str): ")
                    player.name = to_set.upper()
                    input("name set. enter to continue")
                case 4:
                    pass
        
        case 3:
            player.football_minigame()
            input ("enter to continue . . .  ")

        case 4:
            to_continue = True
        case 5:
            sys.exit(1)

    if (not to_continue): dev_mode()