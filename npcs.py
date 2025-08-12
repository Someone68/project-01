import simpleaudio
from utils import *

# load sounds
talking_sounds = [
  simpleaudio.WaveObject.from_wave_file("assets/talkingsound_1.wav"),
  simpleaudio.WaveObject.from_wave_file("assets/talkingsound_2.wav"),
  simpleaudio.WaveObject.from_wave_file("assets/talkingsound_3.wav"),
  simpleaudio.WaveObject.from_wave_file("assets/talkingsound_4.wav"),
  simpleaudio.WaveObject.from_wave_file("assets/talkingsound_5.wav"),
]

class Npc:
  def __init__(self, name, defname = None, talking_sound = None, color = "white"):
    self.name = name
    if (not defname): self.defname = name
    else: self.defname = defname
    self.memory = {}
    self.name_unlocked = False
    self.talking_sound = talking_sound
    self.color = color

    
  def talk(self, text, wait_for_input = True):
    width=30
    height=5
    h_align="left"
    v_align="top"
    padding=1
    title=self.name if self.name_unlocked else self.defname
    color=self.color
    speed=0.01
    cursor.hide()

    def tprint_line(line, row, col):   
      sys.stdout.write(f"\033[{row};{col}H")  # move to row, col
      for char in line:
          print(colored(char, color) if color else char, end='', flush=True)
          talking_sounds[self.talking_sound].play()
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

people = {
  "ms_finessa" : Npc("Ms. Finessa", "Teacher", 0, "light_yellow")
}