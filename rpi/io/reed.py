import RPi.GPIO as gpio
import time

PIN_1 = 12
PIN_2 = 35
gpio.setmode(gpio.BOARD)
gpio.setup(PIN_1, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(PIN_2, gpio.IN, pull_up_down=gpio.PUD_UP)

print "Setup succesful"

stateMapper = { False: 'piece present', True: 'empty field' }

nextState_1 = False
nextState_2 = False
while True:
    if gpio.input(PIN_1) == nextState_1:
        print "State_1 changed to :" + stateMapper[nextState_1]
        nextState_1 = not nextState_1
    if gpio.input(PIN_2) == nextState_2:
        print "State_2 changed to: " + stateMapper[nextState_2]
        nextState_2 = not nextState_2
    time.sleep(0.3)
