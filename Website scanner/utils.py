import sys
import time
from colorama import Fore, Style, init

init()

def print_slow(text, delay=0.03):
    for char in text:
        sys.stdout.write(Fore.CYAN + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def show_loading_bar(label="Chargement", seconds=5):
    print(Fore.YELLOW + f"{label}..." + Style.RESET_ALL)
    for _ in range(seconds):
        sys.stdout.write(Fore.GREEN + "█" + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(1)
    print("\n")
