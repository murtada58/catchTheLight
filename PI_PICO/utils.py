from random import choice

def getRandomInt(start, end, exclude):
    return choice([i for i in range(start, end) if i not in exclude])
        
        
def getRandomIntArray(start, end, length):
    arr = [None] * length
    for i in range(length):
        arr[i] = getRandomInt(start, end, arr)
    return arr

def updateLeds(LEDS, selected):
    for i, LED in enumerate(LEDS):
        LED.value(i in selected)
        
def turnOffAllLeds(PLAYERS):
    for PLAYER in PLAYERS:
        updateLeds(PLAYER["LEDS"], [])
        
def turnOnAllPlayerLeds(PLAYER):
    updateLeds(PLAYER["LEDS"], getRandomIntArray(0, len(PLAYER["LEDS"]), len(PLAYER["LEDS"])))
        
def resetPlayers(PLAYERS, NUM_SELECTED):
    for PLAYER in PLAYERS:
        PLAYER["SCORE"] = 0
        PLAYER["SELECTED"] = getRandomIntArray(0, len(PLAYER["LEDS"]), NUM_SELECTED)
        updateLeds(PLAYER["LEDS"], [])

def displayPlayerScores(lcd, PLAYERS):
    for PLAYER in PLAYERS:
        lcd.putstr(PLAYER["NAME"] + " SCORE: " + str(PLAYER["SCORE"]) + "\n")
        
def displayAndReturnWinners(lcd, PLAYERS):
    # sort desc
    sortedPlayers = sorted(PLAYERS, key = lambda PLAYER : -PLAYER["SCORE"]) 
    if sortedPlayers[0]["SCORE"] == sortedPlayers[1]["SCORE"]:
        lcd.putstr("{:^20}".format("TIE!!!"))
    else:
        lcd.putstr("{:^20}".format(sortedPlayers[0]["NAME"] + " WINS!!!"))
        
    return [PLAYER for PLAYER in sortedPlayers if PLAYER["SCORE"] == sortedPlayers[0]["SCORE"]]
