import os
import sys
import shutil
import time
from PIL import Image
import numpy as np

# Clears the terminal screen depending on the OS
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Returns ANSI escape codes for setting foreground and background colors
def ansi_color(fg, bg):
    return f"\033[38;5;{fg}m\033[48;5;{bg}m"

# Gets the current terminal size (columns, lines)
def get_terminal_size():
    return shutil.get_terminal_size()

# Converts an RGB color to a 256-color ANSI color code
def rgb_to_ansi(r, g, b):
    return 16 + (36 * int(r / 51)) + (6 * int(g / 51)) + int(b / 51)

# Loads and resizes the image to fit the terminal dimensions
def load_image(image_path, term_w, term_h):
    img = Image.open(image_path).convert('RGB')
    scale = min(term_w / img.width, (term_h * 2) / img.height)  # Multiply height by 2 to compensate for terminal character aspect ratio. 1 character is 2 pixels
    new_size = (max(1, int(img.width * scale)), max(1, int(img.height * scale)))
    return np.array(img.resize(new_size, Image.LANCZOS))

# Prints the image in the terminal
def print_image(img):
    for y in range(0, img.shape[0], 2):
        for x in range(img.shape[1]):
            top = img[y][x]
            if y + 1 < img.shape[0]:
                bottom = img[y + 1][x]
            print(f"{ansi_color(rgb_to_ansi(*top), rgb_to_ansi(*bottom))}▀\033[0m", end='')  # Top color = fg, bottom = bg
        print()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <image_path>")
        return

    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        return

    clear_screen()
    prev_w, prev_h = get_terminal_size()
    img = load_image(image_path, prev_w, prev_h)
    print_image(img)

    # Loop to detect terminal resize and re-render the image if needed
    while True:
        w, h = get_terminal_size()
        if (w, h) != (prev_w, prev_h):
            clear_screen()
            prev_w, prev_h = w, h
            img = load_image(image_path, w, h)
            print_image(img)
        time.sleep(0.1)

if __name__ == "__main__":
    main()
