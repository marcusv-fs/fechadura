import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(8, GPIO.OUT)

GPIO.output(8, GPIO.LOW)
time.sleep(3)

GPIO.cleanup()

print("Sucesso")