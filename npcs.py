import json
import re

from termcolor import cprint
from utils import *

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

    # Print ▼ arrow on last content line, second to last column
    arrow_row = start_row + 1 + top_pad + len(aligned_lines)
    arrow_col = width - 2
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
#NPC.add(Npc("Ms. Finessa", "Teacher", 0, "light_yellow"))
#NPC.add(Npc("FJock", "Tuff-Looking Kid", 0, "light_yellow"))
NPC.add(Npc("FJock", "Tuff-Looking Kid", "yellow"))
NPC.add(Npc("Ms. Finessa", "Teacher", "magenta"))


class Interaction:
    def __init__(self, filepath, npc_registry, player):
        self.filepath = filepath
        self.npc_registry = npc_registry
        self.player = player
        self.data = None
        self.default_npc = None

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

        if action_type == "talk":
            npc = self.npc_registry.get(action.get("npc")) if action.get("npc") else self.default_npc
            npc.talk(self.format_text(action["text"]), action.get("wait_for_input", True))

        elif action_type == "play_interaction":
            self.play_file("interactions/" + action.get("interaction"))

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

            caption_indicies = []
            for opt in options:
                if (opt["type"] == "caption"):
                    caption_indicies.push(options.index(opt))
                    if (selected_index == options.index(opt)): selected_index += 1

            while True:
                if len(options) <= 0:
                    break

                # Show menu title (optional)
                if menu_title:
                    if menu_typeout:
                        tprint(self.format_text(menu_title), menu_color)
                    else:
                        cprint(self.format_text(menu_title), menu_color)



                # Build the options list for your select_menu function
                option_labels = [self.format_text(opt["name"]) for opt in options]

                # Call your custom select menu
                idx = select_menu(option_labels, caption_indicies=option_labels)
                cls_fancy()

                chosen = options[idx]
                self.run_action(chosen["action"])

                if chosen.get("stop_finish_code") is True:
                    # input("[DEBUG] STOPPING FINISH CODE ")
                    stop_finish_code = True
                elif chosen.get("stop_finish_code") is False:
                    # input("[DEBUG] USING FINISH CODE ")
                    stop_finish_code = False

                if chosen.get("one_time", True):
                    # input("[DEBUG] ONE TIME - POPPING ")
                    options.pop(idx)

                if chosen.get("end_menu", False):
                    # input("[DEBUG] ENDING MENU ")
                    break

                if len(options) <= options_to_stop:
                    # input("[DEBUG] NO MORE OPTIONS ENDING MENU")
                    break

                if not repeat:
                    break

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
            print("change_select_menu_option would modify menu here (requires context)")

        elif action_type == "comment":
            pass

        else:
            raise ValueError(f"Unknown interaction type: {action_type}")

        cls_fancy()

    @staticmethod
    def play_file(filepath, npc_registry, player):
      inter = Interaction(filepath, npc_registry, player)
      inter.load()
      inter.play()
