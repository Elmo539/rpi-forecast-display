import display_utils as du
import RPi.GPIO as gpio
from Adafruit_CharLCD import Adafruit_CharLCD as LCD
from time import sleep
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
        du.exceptionHandler('No exception', term_msg)
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
                    if datetime.now().minute != 2: # Restart timeframe is the entire 5th minute of every hour.
                        restart_permission = 1
                    else:
                        pass

                    # Checks if we are in the restart timeframe and if the permission flag is set.
                    # If True, the restart_flag is set, signaling a restart.
                    # First clause of this if-statement may not be necessary, to be considered.
                    if (datetime.now().minute == 2) and (restart_permission == 1):
                        restart_flag = 1
                    else:
                        pass

                    # Checks if restart_flag is set, if it is, 'main()' function restarts.
                    # GPIO pins are cleaned up first so that they can be set again.
                    if restart_flag == 1:
                        if (datetime.now().hour == 0):
                            du.restartPrep()
                            du.dayEndLogCleanup()
                        else:
                            du.restartPrep()
                        main()
                    else:
                        pass

                    # Displays the title and data on the LCD for 4 seconds.
                    global lcd
                    du.lcd.clear()
                    du.lcd.message(title_list[i] + max_min_list[i])
                    print(title_list[i] + max_min_list[i])
                    sleep(4)

                # Cleans everything up in case of Ctrl-c.
                except KeyboardInterrupt as e:
                    exception = str(e)
                    term_msg = 'KeyboardInterrupt'
                    du.exceptionHandler(exception, term_msg)
                    return

    # Cleans everything up in case of Ctrl-c.
    except KeyboardInterrupt as e:
        exception = str(e)
        term_msg = 'KeyboardInterrupt'
        du.exceptionHandler(exception, term_msg)
        return


def main():

    # Logging the start of the program.
    du.setup()


    # Setting the 'restart_permission' flag which will only
    # allow the program to restart once during the whole minute.
    global restart_permission
    restart_permission = 1
    if datetime.now().minute == 2:
        restart_permission = 0
    else:
        pass


    # Calling the 'displaySetup()' function to initialize the LCD display.
    du.displaySetup()


    # Running the webscraper
    du.lcd.message("Starting\nwebscraper...")
    print("\nStarting webscraper...")
    global ws
    import webscraper_source as ws


    # Displaying the IP address on the LCD while the program is importing
    # the data. This is mainly for using SSH when debugging.
    du.displayIP()


    # Importing the data from the webscraper. This process is not instantaneous.
    global data
    data = ws.main()


    # Running the format and display functions. 'displayData()' will run continuously.
    try:
        formatData()
        displayData()
    except Exception as e:
        exception = str(e)
        term_msg = 'Error in "display_scrapings.main()" while trying to call "formatData()" and "displayData()".'
        du.exceptionHandler(exception, term_msg)



if __name__ == "__main__":
    main()

