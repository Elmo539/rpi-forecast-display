import display_scrapings as ds
import traceback
import os
from datetime import datetime
from time import sleep
import RPi.GPIO as gpio
from Adafruit_CharLCD import Adafruit_CharLCD as LCD


def setup():
    the_date = datetime.now().strftime("%Y-%m-%d")
    the_time = datetime.now().strftime("%H:%M:%S")

    global error_incident_flag
    error_incident_flag = 0

    global session_file
    session_file = f'session_logs/session_file_{the_date}__{the_time}'

    setup.ext_outfile = f'session_logs/hourly_log_{the_date}__{the_time}'

    global outfile
    outfile = f'session_logs/hourly_log_{the_date}__{the_time}'
    with open(outfile, 'a') as f:
        f.write(f'\nSession started on {the_date} at {the_time}.')
        ip_address = os.popen('hostname -I').read()
        f.write(f'\nSession IP: {ip_address}')
        f.write(f'\nerror_incident_flag set to {error_incident_flag}.')


def displaySetup():
    try:
        gpio.setmode(gpio.BCM)
        global lcd
        lcd = LCD(rs=26, en=19, d4=13, d5=6, d6=5, d7=11, cols=16, lines=2)

        lcd.clear()
        print("\ndisplay ready.")
        return lcd

    except Exception as e:
        exception = traceback.format_exc()
        term_msg = 'Error in LCD setup'
        exceptionHandler(1, exception, term_msg)


def exceptionHandler(restart, exc, term_message):
    os.popen('sudo pkill chromium')

    global error_incident_flag
    error_incident_flag += 1

    global outfile
    with open(outfile, 'a') as f:
        the_time = datetime.now().strftime("%H:%M:%S")
        f.write('\n\n--- ' + str(datetime.now()) + ' ---\n')
        f.write(term_message + '\n')
        f.write(f'\nError number {error_incident_flag}.')
        f.write(f'\nAn error occured at {the_time}.')
        f.write(f'\n{exc}')

    global std_outfile
    std_outfile = outfile + '%' + str(error_incident_flag)
    os.rename(outfile, std_outfile)

    if restart == 1:
        with open(std_outfile, 'a') as f:
            f.write('\nRebooting...')
        sleep(10)
        progRestart(1, 0, std_outfile)
    else:
        with open(std_outfile, 'a') as f:
            f.write('\nShouldn\'t restart.')
        global lcd
        lcd.clear()
        gpio.cleanup()
        quit()


def displayIP():
    global lcd
    lcd.clear()
    ip_address = os.popen('hostname -I').read()
    lcd.message(str(ip_address))
    print('\nDisplaying IP...')


def progRestart(is_error_flag, day_end_flag, current_outfile):
    os.popen('sudo pkill chromium')
    the_date = datetime.now().strftime("%Y-%m-%d")
    the_time = datetime.now().strftime("%H:%M:%S")

    std_outfile = current_outfile
    with open(std_outfile, 'a') as f:
        f.write('\n\n--- RESTART ---\n')
        f.write(f'restarting at {the_date} -- {the_time}.')

    global error_incident_flag
    if error_incident_flag != 0:
        with open(std_outfile, 'a') as f:
            restart_time = datetime.now().strftime("%H:%M:%S")
            f.write(f'\nSession restarted at {restart_time} with {error_incident_flag} error(s).')
    else:
        with open(std_outfile, 'a') as f:
            restart_time = datetime.now().strftime("%H:%M:%S")
            f.write(f'\nSession restarted at {restart_time} with no errors.')

    swap_files = str(os.popen("grep Swap /proc/meminfo | awk '{ print ($2) }'").read()).removesuffix('\n')
    with open(std_outfile, 'a') as f:
        f.write(f'\nSwap space used: {swap_files} kB.')

    mem_available = str(os.popen("grep MemAvailable /proc/meminfo | awk '{ print ($2) }'").read()).removesuffix('\n')
    if int(mem_available) < 200000:
        with open(std_outfile, 'a') as f:
            f.write('\nAvailable memory is less than 200,000 kB. System rebooting...')
        os.popen('sudo reboot')
    else:
        with open(std_outfile, 'a') as f:
            f.write(f'\nAvailable memory at end of session: {int(mem_available)} kB.')

    if day_end_flag == 1:
        try:
            dayEndLogCleanup()
        except Exception as e:
            exception = traceback.format_exc()
            term_msg = 'Error calling dayEndLogCleanup() in progRestart().'
            exceptionHandler(1, exception, term_msg)
    elif is_error_flag == 1:
        os.popen('sudo reboot')
    else:
        global lcd
        lcd.clear()
        gpio.cleanup()


def dayEndLogCleanup():
    the_day = int(datetime.now().strftime("%d"))
    the_day = the_day - 1
    the_date = datetime.now().strftime(f"%Y-%m-{the_day}")

    error_logs = []

    logs = os.scandir('session_logs')
    with logs as logs:
        for l in logs:
            name = l.name
            if (the_date in name) and ('hourly_log' in name):
                print(f'clean hourly log found: {name}')
                os.remove(f'session_logs/{name}')
            else:
                error_logs.append(name)

        f.write(f'\nDay: {the_date}')
        f.write(f'\nDay completed with {error_incident_flag} error(s).')


    with open(day_file, 'a') as f:
        f.write(f'\nLog entered at {datetime.now.strftime("%Y-%m-%d: %H:%M:%S")}')

