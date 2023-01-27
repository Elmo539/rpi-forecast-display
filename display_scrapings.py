import traceback
import os
import RPi.GPIO as gpio
from Adafruit_CharLCD import Adafruit_CharLCD as LCD
from time import sleep
from time import time
from datetime import datetime


# Function to strip out the data from the packet received from the webscraper.
def formatData():
    print("\nFormatting data...")
    # Had problems with website not processing request properly.
    # This if-statement exits the program if the data is an
    # unexpected amount, indicating we didn't get the webpage
    # we were expecting. Also for logging purposes.
    if len(data['hours']['data']) != 16:
        term_msg = 'Length of "Hours" list was an unexpected value.\nCheck website functionality.'
        lcd_msg = 'WebscraperError'
        exceptionHandler('No exception', term_msg, lcd_msg)
    else:
        pass

    # Gets the max and min values from each dataset.
    global max_hours
    max_hours = data['hours']['data'][-1]
    global min_hours
    min_hours = data['hours']['data'][0]
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

    # Create the list of titles for the data.
    global title_list
    title_list = ['Hours(range)\n','Temperature(F)\n', 'Dewpoint(F)\n', 'Wind(mph)\n', 'Skycover(%)\n', 'Precipitation(%)\n']
    # Put all the max and min values into a list for iterating over.
    global max_min_list
    max_min_list = [
        f'start:{min_hours}  end:{max_hours}\n',
        f'max:{max_temp}    min:{min_temp}\n',
        f'max:{max_dewpt}    min:{min_dewpt}\n',
        f'max:{max_wind}    min:{min_wind}\n',
        f'max:{max_skycover}    min:{min_skycover}\n',
        f'max:{max_precip}    min:{min_precip}\n',
    ]


# Displays the data on the LCD. Much of the complexity
# in this code refers to the restart function.
def displayData():
    print("\nDisplaying...\n")

    try:
        restart_flag = 0 # 'restart_flag' is disabled on startup.
        while True:
            for i in range(len(title_list)):
                # This try - except block checks to see if it is
                # time to restart the webscraper.
                try:
                    # Re-enables the 'restart_permission' flag after the
                    # restart timeframe has passed. This is necessary because
                    # the 'main()' function will check to see if we are in the
                    # restart timeframe. If we are, the program will assume that
                    # it has already restarted and the 'restart_permission' flag
                    # will be set to 0.
                    global restart_permission
                    if datetime.now().minute != 5: # Restart timeframe is the entire 5th minute of every hour.
                        restart_permission = 1
                    else:
                        pass

                    # Checks if we are in the restart timeframe and if the permission flag is set.
                    # If True, the restart_flag is set, signaling a restart.
                    # First clause of this if-statement may not be necessary, to be considered.
                    if (datetime.now().minute == 5) and (restart_permission == 1):
                        restart_flag = 1
                    else:
                        pass

                    # Checks if restart_flag is set, if it is, 'main()' function restarts.
                    # GPIO pins are cleaned up first so that they can be set again.
                    if restart_flag == 1:

                        with open(outfile, 'a') as f:
                            restart_time = datetime.now().strftime("%H %M %S")
                            f.write(f'\nSession restarted at {restart_time}.')
                        gpio.cleanup()
                        main()
                    else:
                        pass

                    # Displays the title and data on the LCD for 4 seconds.
                    global lcd
                    lcd.clear()
                    lcd.message(title_list[i] + max_min_list[i])
                    print(title_list[i] + max_min_list[i])
                    sleep(4)

                # Cleans everything up in case of Ctrl-c.
                except KeyboardInterrupt as e:
                    exception = str(e)
                    term_msg = 'KeyboardInterrupt'
                    lcd_msg = 'Keybrd Interrupt'
                    exceptionHandler(exception, term_msg, lcd_msg)
                    return

    # Cleans everything up in case of Ctrl-c.
    except KeyboardInterrupt as e:
        exception = str(e)
        term_msg = 'KeyboardInterrupt'
        lcd_msg = 'Keybrd Interrupt'
        exceptionHandler(exception, term_msg, lcd_msg)
        return


# Initializes the GPIO pins and the LCD display.
def displaySetup():
    print("\nstarting display...")

    try:
        gpio.setmode(gpio.BCM)
        global lcd
        lcd = LCD(rs=26, en=19, d4=13, d5=6, d6=5, d7=11, cols=16, lines=2)

        lcd.clear()
        print("\ndisplay ready.")

    except Exception as e:
        exception = str(e)
        term_msg = 'Error in LCD setup'
        lcd_msg = 'LcdSetupError'
        exceptionHandler(exception, term_msg, lcd_msg)


# Gets the IP address of the RPi and displays it on
# the LCD for easier debugging with SSH. This project
# was originally developed on a college campus, so a
# static IP was not possible. This may not be needed if
# you are able to set a static IP for the RPi.
def displayIP():
    global lcd
    lcd.clear()
    ip_address = os.popen('hostname -I').read()
    lcd.message(str(ip_address))
    print('\nDisplaying IP...')


# Function for handling errors. Logs the traceback into a 'log.txt'
# file, displays the error on the LCD, and then cleans up the GPIO pins.
def exceptionHandler(exc, term_message, lcd_message):
    global outfile
    with open(outfile, 'a') as f:
        f.write('\n\n--- ' + str(datetime.now()) + ' ---\n')
        f.write(term_message + '\n')
        f.write(traceback.format_exc())
    global lcd
    if exc == 'KeyboardError':
        lcd.clear()
        lcd.message(lcd_message)
        sleep(10)
    else:
        lcd.clear()
        gpio.cleanup()


# Logs the beginning of the session.
def sessionLog():
    the_date = datetime.now().strftime("%Y %m %d")
    the_time = datetime.now().strftime("%H %M %S")

    global outfile
    outfile = f'session_logs/{the_date}__{the_time}'
    with open(outfile, 'a') as f:
        f.write(f'\nSession started on {the_date} at {the_time}.')
        ip_address = os.popen('hostname -I').read()
        f.write(f'\nSession IP: {ip_address}')


def main():

    # Logging the start of the program.
    sessionLog()

    # Setting the 'restart_permission' flag which will only
    # allow the program to restart once during the whole minute.
    global restart_permission
    restart_permission = 1
    if datetime.now().minute == 5:
        restart_permission = 0
    else:
        pass

    # Calling the 'displaySetup()' function to initialize the LCD display.
    displaySetup()

    # Running the webscraper
    global lcd
    lcd.message("Starting\nwebscraper...")
    print("\nStarting webscraper...")
    import webscraper_source as ws

    # Displaying the IP address on the LCD while the program is importing
    # the data. This is mainly for using SSH when debugging.
    displayIP()

    # Importing the data from the webscraper. This is not instantaneous.
    global data
    data = ws.main()
    # Running the format and display functions. 'displayData()' will run continuously.
    try:
        formatData()
        displayData()
    except Exception as e:
        exception = str(e)
        term_msg = 'Error in "display_scrapings.main()" while trying to call "formatData()" and "displayData()".'
        lcd_msg = 'MainDisplayError'
        exceptionHandler(excpetion, term_msg, lcd_msg)


if __name__ == "__main__":
    main()

