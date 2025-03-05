from random import choice

def getRandomInt(start, end, exclude):
    return choice([i for i in range(start, end) if i not in exclude])
        
        
def getRandomIntArray(start, end, length):
    arr = [None] * length
    for i in range(length):
        arr[i] = getRandomInt(start, end, arr)
    return arr

def manageLights(LEDS, selected):
    for i, LED in enumerate(LEDS):
        LED.value(i in selected)