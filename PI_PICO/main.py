from machine import I2C, Pin
from time import time, sleep
from random import choice
from pico_i2c_lcd import I2cLcd
from utils import getRandomInt, getRandomIntArray, updateLeds, resetPlayers, displayPlayerScores, displayAndReturnWinners, turnOffAllLeds, turnOnAllPlayerLeds

NUM_SELECTED = 2
COUNTDOWN_DURATION = 3
GAME_DURATION = 30
WINNER_FLASH_DURATION = 1

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 4, 20)

START_BUTTON = Pin(2, Pin.IN, Pin.PULL_DOWN)

PLAYERS = [
    {
        "NAME": "P1",
        "LEDS": [
            Pin(16, Pin.OUT),
            Pin(17, Pin.OUT),
            Pin(18, Pin.OUT)
        ],
        "BUTTONS": [
            Pin(15, Pin.IN, Pin.PULL_DOWN),
            Pin(14, Pin.IN, Pin.PULL_DOWN),
            Pin(13, Pin.IN, Pin.PULL_DOWN)
        ],
        "SCORE": 0,
        "SELECETD": []
    },
    {
        "NAME": "P2",
        "LEDS": [
            Pin(6, Pin.OUT),
            Pin(7, Pin.OUT),
            Pin(8, Pin.OUT)
        ],
        "BUTTONS": [
            Pin(3, Pin.IN, Pin.PULL_DOWN),
            Pin(4, Pin.IN, Pin.PULL_DOWN),
            Pin(5, Pin.IN, Pin.PULL_DOWN)
        ],
        "SCORE": 0,
        "SELECETD": []
    },
]

lcd.putstr("{:^20}".format("PRESS START BUTTON"))
lcd.putstr("{:^20}".format("TO PLAY"))
resetPlayers(PLAYERS, NUM_SELECTED)

started = False
start_time = 0
next_update_time = 0
score_needs_update = False
winners = None
next_flash_time = 0
is_flash_on = False

# Currently too slow sometimes inputs are being missed!!!
while True:
    curr_time = time()
    if started:
        for PLAYER in PLAYERS:
            SELECTED = PLAYER["SELECTED"]
            LEDS = PLAYER["LEDS"]
            updateLeds(LEDS, SELECTED)
            for i, num in enumerate(SELECTED):
                if PLAYER["BUTTONS"][num].value():
                    score_needs_update = True
                    PLAYER["SCORE"] += 1
                    SELECTED[i] = getRandomInt(0, len(LEDS), SELECTED)
        
        if score_needs_update or next_update_time <= curr_time:
            lcd.clear()
            displayPlayerScores(lcd, PLAYERS)
            lcd.putstr("TIME REMAINING: " + str((start_time + GAME_DURATION - curr_time) // 1) + "\n")
            next_update_time = (curr_time + 1) // 1
            score_needs_update = False

        if start_time + GAME_DURATION <= curr_time:
            started = False
            lcd.clear()
            displayPlayerScores(lcd, PLAYERS)
            winners = displayAndReturnWinners(lcd, PLAYERS)
            turnOffAllLeds(PLAYERS)

    # flashing effect for winning players
    if winners is not None and next_flash_time <= curr_time:
        if is_flash_on:
            turnOffAllLeds(PLAYERS)
        else:
            for winner in winners:
                turnOnAllPlayerLeds(winner)
        is_flash_on = not is_flash_on
        next_flash_time = curr_time + WINNER_FLASH_DURATION
        

    if START_BUTTON.value():
        for i in range(COUNTDOWN_DURATION, 0, -1):
            lcd.clear()
            lcd.putstr("{:^20}".format("STARTING IN: " + str(i) + "!"))
            sleep(1)
        resetPlayers(PLAYERS, NUM_SELECTED)
        winner = None
        started = True
        curr_time = time()
        start_time = curr_time
        next_update_time = curr_time
        lcd.putstr("\n") # No idea why but if this isn't here the first print on line 74 shows on 1 line instead of being split with the new lines

