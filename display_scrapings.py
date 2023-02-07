import display_utils as du
import traceback
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
        print('Length of hours[] was not standard.')
        term_msg = 'Length of "Hours" list was an unexpected value.\nCheck website functionality.'
        du.exceptionHandler(1, 'No exception', term_msg)
        main()
    else:
        pass

    # Gets the max and min values from each dataset.
    global max_hours
    max_hours = "{0:0>2}".format(data['hours']['data'][-1])
    global min_hours
    min_hours = "{0:0>2}".format(data['hours']['data'][0])
    global max_temp
    max_temp = "{0:0>2}".format(data['temps']['max'])
    global min_temp
    min_temp = "{0:0>2}".format(data['temps']['min'])
    global max_dewpt
    max_dewpt = "{0:0>2}".format(data['dewpoints']['max'])
    global min_dewpt
    min_dewpt = "{0:0>2}".format(data['dewpoints']['min'])
    global max_wind
    max_wind = "{0:0>2}".format(data['winds']['max'])
    global min_wind
    min_wind = "{0:0>2}".format(data['winds']['min'])
    global max_skycover
    max_skycover = "{0:0>2}".format(data['skycover']['max'])
    global min_skycover
    min_skycover = "{0:0>2}".format(data['skycover']['min'])
    global max_precip
    max_precip = "{0:0>2}".format(data['precip']['max'])
    global min_precip
    min_precip = "{0:0>2}".format(data['precip']['min'])

    # Create the list of titles for the data.
    global title_list
    title_list = ['Hours(range)\n','Temperature(F)\n', 'Dewpoint(F)\n', 'Wind(mph)\n', 'Skycover(%)\n', 'Precipitation(%)\n']
    # Put all the max and min values into a list for iterating over.
    global l_reg_list
    l_reg_list = [
        f'{min_hours}',
        f'{min_temp}',
        f'{min_dewpt}',
        f'{min_wind}',
        f'{min_skycover}',
        f'{min_precip}',
    ]
    global r_reg_list
    r_reg_list = [
        f'{max_hours}\n',
        f'{max_temp}\n',
        f'{max_dewpt}\n',
        f'{max_wind}\n',
        f'{max_skycover}\n',
        f'{max_precip}\n',
    ]


# Displays the data on the LCD. Much of the complexity
# in this code refers to the restart function.
def displayData():
    print("\nDisplaying...\n")

    restart_flag = 0 # 'restart_flag' is disabled on startup.
    while True:
        for i in range(len(title_list)):
            try:
                global restart_permission
                if debug_mode_flag == 1:
                    if (datetime.now().minute % 5) != 0: # Restart timeframe is the entire 5th minute of every hour.
                        restart_permission = 1
                    else:
                        pass
                    if ((datetime.now().minute % 5) == 0) and (restart_permission == 1):
                        raise NameError
                        restart_flag = 1
                    else:
                        pass

                else:
                    if (datetime.now().minute) != 2: # Restart timeframe is the entire 5th minute of every hour.
                        restart_permission = 1
                    else:
                        pass
                    if ((datetime.now().minute) == 2) and (restart_permission == 1):
                        restart_flag = 1
                    else:
                        pass

                if restart_flag == 1:
                    if (datetime.now().hour == 0):
                        outfile = du.setup.ext_outfile
                        du.progRestart(0, 1, outfile)
                        main()
                    else:
                        outfile = du.setup.ext_outfile
                        du.progRestart(0, 0, outfile)
                        main()
                else:
                    pass

                try:
                    line_1 = title_list[i]

                    the_time = datetime.now().strftime("%H%M")
                    line_2 = l_reg_list[i] + f'    {the_time}    ' + r_reg_list[i]
                    global lcd
                    du.lcd.clear()
                    du.lcd.message(line_1 + line_2)
                    print(line_1 + line_2)
                    sleep(4)
                except (Exception, KeyboardInterrupt) as e:
                    exception = traceback.format_exc()
                    print(f'Exception in lcd function:\nERROR: {exception}')
                    term_msg = 'Exception in lcd function.'
                    du.exceptionHandler(0, exception, term_msg)

            # Cleans everything up in case of Ctrl-c.
            except (Exception, KeyboardInterrupt) as e:
                exception = traceback.format_exc()
                print(f'Exception in displayData():\nERROR: {exception}')
                term_msg = 'Exception in displayData().'
                du.exceptionHandler(0, exception, term_msg)


def main():
    global debug_mode_flag
    debug_mode_flag = 0

    # Logging the start of the program.
    du.setup()


    # Setting the 'restart_permission' flag which will only
    # allow the program to restart once during the whole minute.
    global restart_permission
    restart_permission = 1
    if debug_mode_flag == 1:
        if (datetime.now().minute % 5) == 0:
            restart_permission = 0
        else:
            pass
    else:
        if (datetime.now().minute) == 2:
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
    formatData()
    displayData()



if __name__ == "__main__":
    main()

