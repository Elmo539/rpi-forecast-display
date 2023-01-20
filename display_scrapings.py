import traceback
import os
import RPi.GPIO as gpio
from Adafruit_CharLCD import Adafruit_CharLCD as LCD
from time import sleep
from time import time
from datetime import datetime


def dark_button(parameter):
    print('dark_button pressed with paramerter', parameter)
    swap = {0:1, 1:0}

    global lcd_light_flag
    lcd_light_flag = swap[lcd_light_flag]

    if lcd_light_flag == 0:
        gpio.output(10, False)
    elif lcd_light_flag == 1:
        gpio.output(10, True)
    else:
        pass

    return lcd_light_flag


def formatData():
    print("\nPacket imported.")
    print("\nFormatting data...")
    global max_hours
    try:
        max_hours = data['hours']['data'][-1]
    except IndexError:
        max_hours = 'na'
    global min_hours
    try:
        min_hours = data['hours']['data'][0]
    except IndexError:
        min_hours = 'na'
    global max_temp
    max_temp = data['temps']['max']
    global min_temp
    min_temp = data['temps']['min']
    global max_dewpt
    max_dewpt = data['dewpoints']['max']
    global min_dewpt
    min_dewpt = data['dewpoints']['min']
    global max_wind
    max_wind = data['winds']['max']
    global min_wind
    min_wind = data['winds']['min']
    global max_skycover
    max_skycover = data['skycover']['max']
    global min_skycover
    min_skycover = data['skycover']['min']
    global max_precip
    max_precip = data['precip']['max']
    global min_precip
    min_precip = data['precip']['min']

    global title_list
    title_list = ['Hours(range)\n','Temperature(F)\n', 'Dewpoint(F)\n', 'Wind(mph)\n', 'Skycover(%)\n', 'Precipitation(%)\n']
    global max_min_list
    max_min_list = [
        f'start:{min_hours}  end:{max_hours}\n',
        f'max:{max_temp}    min:{min_temp}\n',
        f'max:{max_dewpt}    min:{min_dewpt}\n',
        f'max:{max_wind}    min:{min_wind}\n',
        f'max:{max_skycover}    min:{min_skycover}\n',
        f'max:{max_precip}    min:{min_precip}\n',
    ]


def displayData():
    print("\nDisplaying...\n")

    button_pin = 9
    gpio.setup(button_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.add_event_detect(button_pin, gpio.BOTH, callback=dark_button, bouncetime=400)

    try:
        restart_flag = 0
        while True:
            for i in range(len(title_list)):
                try:
                    global restart_permission
                    if ((datetime.now().minute % 20) == 0) and (restart_permission == 1):
                        restart_flag = 1
                    else:
                        pass
                    if restart_flag == 1:
                        gpio.remove_event_detect(button_pin)
                        gpio.cleanup()
                        main()
                    else:
                        pass
                    global lcd
                    lcd.clear()
                    lcd.message(title_list[i] + max_min_list[i])
                    print(title_list[i] + max_min_list[i])
                    sleep(4)
                except KeyboardInterrupt:
                    lcd.clear()
                    gpio.cleanup()
                    return

    except KeyboardInterrupt:
        lcd.clear()
        gpio.cleanup()
        return


def main():
    global restart_permission
    restart_permission = 1
    if (datetime.now().minute % 20) == 38:
        restart_permission = 0
    else:
        pass
    print("\nstarting display...")

    try:
        gpio.setmode(gpio.BCM)
        global lcd
        lcd = LCD(rs=26, en=19, d4=13, d5=6, d6=5, d7=11, cols=16, lines=2)

        global lcd_light_flag
        lcd_light_flag = 0

        global start_flag
        start_flag = 1

        global ip_display_flag
        ip_display_flag = 0

        gpio.setup(10, gpio.OUT)
        gpio.output(10, False)
        lcd.clear()
        print("\ndisplay ready.")

        print("\nstarting webscraper...")
        lcd.message("Starting\nwebscraper...")
    except Exception:
        traceback.print_exc()
        gpio.cleanup()

    import webscraper_source as ws

    lcd.clear()
    print("\nRunning webscraper...")
    lcd.message("Running\nwebscraper...")

    global data
    data = ws.main()
    formatData()

    displayData()


if __name__ == "__main__":
    main()

