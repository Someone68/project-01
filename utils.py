import sys
from time import sleep
from termcolor import colored


def tprint(txt, clr=None, spd=0.05):
    for x in txt:
        print(colored(x, no_color=True if clr == None else False, color=clr if clr != None else None), end='')
        sys.stdout.flush()
        sleep(spd)
    print()

def tinput(txt, clr=None, spd=0.05):
    for x in txt:
        print(colored(x, no_color=True if clr == None else False, color=clr if clr != None else None), end='')
        sys.stdout.flush()
        sleep(spd)
    return input()

def draw_box(
    text,
    width=30,
    height=5,
    h_align="center",
    v_align="center",
    padding=0
):
    if isinstance(text, str):
        lines = text.splitlines()
    else:
        lines = list(text)

    max_line_len = max(len(line) for line in lines)
    usable_width = width - 2 - 2 * padding
    if usable_width < max_line_len:
        raise ValueError("Text too wide for box with given padding.")

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
