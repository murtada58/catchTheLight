from machine import I2C, Pin
from time import time, sleep
from random import choice
from pico_i2c_lcd import I2cLcd
from utils import getRandomInt, getRandomIntArray, manageLights

NUM_SELECTED = 2
COUNTDOWN_TIME = 3
GAME_LENGTH = 30

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 4, 20)

START_BUTTON = Pin(2, Pin.IN, Pin.PULL_DOWN)

# TODO commonise to X number of players using a dict

# PLAYER 1
LEDS = [
    Pin(16, Pin.OUT),
    Pin(17, Pin.OUT),
    Pin(18, Pin.OUT)
]
BUTTONS = [
    Pin(15, Pin.IN, Pin.PULL_DOWN),
    Pin(14, Pin.IN, Pin.PULL_DOWN),
    Pin(13, Pin.IN, Pin.PULL_DOWN)
]

# PLAYER 2
LEDS2 = [
    Pin(6, Pin.OUT),
    Pin(7, Pin.OUT),
    Pin(8, Pin.OUT)
]
BUTTONS2 = [
    Pin(3, Pin.IN, Pin.PULL_DOWN),
    Pin(4, Pin.IN, Pin.PULL_DOWN),
    Pin(5, Pin.IN, Pin.PULL_DOWN)
]


lcd.putstr("PRESS START BUTTON\nTO PLAY")

score = 0
score2 = 0

# turns off all the LEDS
manageLights(LEDS, [])
manageLights(LEDS2, [])

started = False
start_time = 0
next_update_time = 0

while True:
    if started:
        startScore = score
        startScore2 = score2
        manageLights(LEDS, selected)
        manageLights(LEDS2, selected2)
        curr_time = time()
        for i, num in enumerate(selected):
            if BUTTONS[num].value():
                score += 1
                selected[i] = getRandomInt(0, len(LEDS), selected)
                print(score)
                # sleep(0.1) # can probably get rid of this it only really makes sense if planning on subtracting the score, another way would be to only count button presses on push down instead of push up 
            elif any([BUTTON.value() for BUTTON in BUTTONS]):
                # score -= 1
                print(score) 
                # sleep(0.1) # can probably get rid of this it only really makes sense if planning on subtracting the score, another way would be to only count button presses on push down instead of push up
        
        for i, num in enumerate(selected2):
            if BUTTONS2[num].value():
                score2 += 1
                selected2[i] = getRandomInt(0, len(LEDS2), selected2)
                print(score2)
                # sleep(0.1) # can probably get rid of this it only really makes sense if planning on subtracting the score, another way would be to only count button presses on push down instead of push up 
            elif any([BUTTON.value() for BUTTON in BUTTONS2]):
                # score2 -= 1
                print(score2) 
                # sleep(0.1) # can probably get rid of this it only really makes sense if planning on subtracting the score, another way would be to only count button presses on push down instead of push up
            
            
        if startScore != score or startScore2 != score2 or next_update_time <= curr_time:
            lcd.clear() 
            lcd.putstr("P1 SCORE: " + str(score)+"\n")
            lcd.putstr("P2 SCORE: "+str(score2)+"\n")
            lcd.putstr("TIME REMAINING: "+str((start_time + GAME_LENGTH - curr_time) // 1))
            next_update_time = (curr_time + 1) // 1

            
        if start_time + GAME_LENGTH <= curr_time:
            started = False
            lcd.clear()
            lcd.putstr("P1 SCORE: " + str(score)+"\n")
            lcd.putstr("P2 SCORE: "+str(score2)+"\n")
            if score == score2:
                lcd.putstr("TIE!!!")
            elif score > score2:
                lcd.putstr("P1 WINS!!!")
            else :
                lcd.putstr("P2 WINS!!!")
        
    if START_BUTTON.value():
        score = 0
        score2 = 0
        selected = getRandomIntArray(0, len(LEDS), NUM_SELECTED)
        selected2 = getRandomIntArray(0, len(LEDS2), NUM_SELECTED)
        manageLights(LEDS, [])
        manageLights(LEDS2, [])
        for i in range(COUNTDOWN_TIME, 0, -1):
            lcd.clear()
            lcd.putstr("STARTING IN: " + str(i) + "!")
            sleep(1)
        started = True
        curr_time = time()
        start_time = curr_time
        next_update_time = curr_time + 1 // 1
        lcd.clear() 
        lcd.putstr("P1 SCORE: " + str(score)+"\n")
        lcd.putstr("P2 SCORE: "+str(score2)+"\n")
        lcd.putstr("TIME REMAINING: "+str((start_time + GAME_LENGTH - curr_time) // 1))

