# 06_reactions.py

import RPi.GPIO as GPIO
import time, random, math

GPIO.setmode(GPIO.BCM)
red_pin = 18
green_pin = 23
red_switch_pin = 24
green_switch_pin = 25

GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(red_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(green_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def green():
    GPIO.output(green_pin, True)
    GPIO.output(red_pin, False)

def red():
    GPIO.output(green_pin, False)
    GPIO.output(red_pin, True)

def off():
    GPIO.output(green_pin, True)
    GPIO.output(red_pin, True)

def key_pressed():
    if GPIO.input(red_switch_pin) and GPIO.input(green_switch_pin):
        return 0
    if not GPIO.input(red_switch_pin) and not GPIO.input(green_switch_pin):
        return -1
    if not GPIO.input(red_switch_pin) and GPIO.input(green_switch_pin):
        return 1
    if GPIO.input(red_switch_pin) and not GPIO.input(green_switch_pin):
        return 2

n = 0
sum = 0
sumsq = 0
bad = 0

try:        
    while n < 10:
        off()
        print("Press the button for red or green when one lights")
        delay = random.randint(2, 5)
        color = random.randint(1, 2)
        time.sleep(delay)
        if (color == 2):
            red()
        else:
            green()
        t1 = time.time()
        while not key_pressed():
            pass

        if key_pressed() != color :
            bad += 1
            print("WRONG BUTTON")
        else:
            t2 = time.time()
            diff = int((t2 - t1) * 1000)
            n += 1
            sum += diff
            sumsq += diff * diff
            print("Time: " + str(diff) + " milliseconds")
finally:
    if n > 0:
        avg = sum / n
        print("Average = " + str(avg) + ", stddev = " + str(math.sqrt(sumsq / n - avg * avg)))
    if bad > 0:
        print("You have also pushed " + str(bad) + " wrong buttons out of " + str(bad + n))
    print("Cleaning up")
    GPIO.cleanup()
