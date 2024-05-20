# hyonks-atlasbrute
this is my custom-made password bruteforcer <br/>
it was made for the God Sngol lognS ARG but it is technically usable in a lot of places if you configure accordingly<br/>
(DO NOT USE THIS FOR SKETCHY, QUESTIONABLE, OR ILLEGAL USE PLEASE THANKS)<br/>
<br/>
# how the hell do i use it<br/>
shrimple - find your target, and figure out where the password box is<br/>
## ok how do i do that<br/>
take a screenshot of your screen and open it in any editing software (paint(dot)net is my software of choice, but mspaint would work)<br/>
hover your cursor over the center of the login box, and find the position in the image where it is<br/>
take the coordinates, and slot them into `start_password_brute_force` and/or `start_date_brute_force`<br/>
```
def start_password_brute_force():
    global failsafe_thread
    failsafe_thread = threading.Thread(target=check_failsafe)
    failsafe_thread.start()
    max_length = 8  # Change as needed
    login_box_position = (950, 570)  # Replace with the actual position of the login box on your screen
    brute_force_password(max_length, login_box_position)
```
it's the same line for both - `login_box_position`<br/>
<br/>
## cool so now what do i do<br/>
configure your delay<br/>
set `pyautogui.PAUSE = 0.05` to some differing set - this is in seconds, so 0.05 is 50 ms, and one frame (if you have a 60 fps setup) is 0.0167 (16.7 ms)<br/>
personally, i've had it on 0.02 or 0.05 for most things, but you could use a shorter one if using it as an autoclicker/macro or a macro tool (you'd want longer if using for website bruteforcing)<br/>
<br/>
## what passwords will it use?<br/>
with no dictionary, it will either run off a charset and iterate through the list or try a linear series of dates (mm/dd/yyyy, but this is changeable)<br/>
you may want to edit the charset too - possible in main.py<br/>
if you would like to have a list format in plain text with newlines separating the passwords<br/>
