# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import RPi.GPIO as GPIO
import time
import os
import json
from twilio.rest import Client
import requests
#twilio testnumber +12057079430
Tempsensor = '/sys/bus/w1/devices/28-00000b54373c/w1_slave'


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(17,GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

def send_sms(Tempsensor):
    account_sid = "AC2f4da5501b0456a1dbac85dda9eef1e5"
    auth_token = "cc5ec1b500d3538534fe2bfc53184fa4"
    client = Client(account_sid,auth_token)
    temperatures = convertTempsensorData(Tempsensor)
    
    message = "The Temperature at loading station in Berlin is currently {}°C".format(temperatures[0])
    
    message = client.messages.create(to = "(string_of your number)", from_= "(string of number you want a message too)",body = message)
    
    print(message.sid)
    print("Message sent")

def LED_blinking(GPIO_Pin):
    for i in range(5):
        GPIO.output(GPIO_Pin,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(GPIO_Pin,GPIO.LOW)
        time.sleep(0.5)


def readTempSensor(sensorName):
    f = open(sensorName, 'r')
    lines = f.readlines()
    f.close()
    return lines

def convertTempsensorData(Tempsensor):
    lines = readTempSensor(Tempsensor)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = readTempSensor(Tempsensor)
        
    temperatureAt = lines[1].find('t=')   
    if temperatureAt != -1:
        tempData = lines[1][temperatureAt+2:]
        celsius = float(tempData)/1000
        kelvin = celsius + 273.15
        fahrenheit = celsius*(9/5) +32
        
        return celsius, kelvin, fahrenheit
        

if __name__ == '__main__':
    try:
        print("Give an input signal")
        while True:
            if GPIO.input(17) == GPIO.HIGH:
                print("Button has been pressed")
        
                temperatures = convertTempsensorData(Tempsensor)
                if temperatures >= 75:
                    send_sms(Tempsensor)
                print("Die Temperatur beträgt: {} °C, {} K, {} °Fahrenheit".format(temperatures[0], temperatures[1], temperatures[2]))
                print("Watch the LEDs")
                LED_blinking(6)
                LED_blinking(26)
                LED_blinking(19)
                LED_blinking(13)
                print("Party finished")
            temperatures = convertTempsensorData(Tempsensor)
            if temperatures >= 75:
                send_sms(Tempsensor)
        #GPIO.add_event_detect(6, GPIO.BOTH, callback=pressed_button) #GPIO 17
        
        
        

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Goodbye")
