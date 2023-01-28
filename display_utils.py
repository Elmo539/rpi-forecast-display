import traceback
import os
from datetime import datetime
import RPi.GPIO as gpio
from Adafruit_CharLCD import Adafruit_CharLCD as LCD


def setup():
    the_date = datetime.now().strftime("%Y-%m-%d")
    the_time = datetime.now().strftime("%H:%M:%S")

    global outfile
    outfile = f'session_logs/hourly_log_{the_date}__{the_time}'
    with open(outfile, 'a') as f:
        f.write(f'\nSession started on {the_date} at {the_time}.')
        ip_address = os.popen('hostname -I').read()
        f.write(f'\nSession IP: {ip_address}')
    global error_incident_flag
    error_incident_flag = 0


def displaySetup():
    try:
        gpio.setmode(gpio.BCM)
        global lcd
        lcd = LCD(rs=26, en=19, d4=13, d5=6, d6=5, d7=11, cols=16, lines=2)

        lcd.clear()
        print("\ndisplay ready.")
        return lcd

    except Exception as e:
        exception = str(e)
        term_msg = 'Error in LCD setup'
        exceptionHandler(exception, term_msg)


def exceptionHandler(exc, term_message):
    global outfile
    with open(outfile, 'a') as f:
        f.write('\n\n--- ' + str(datetime.now()) + ' ---\n')
        f.write(term_message + '\n')
        f.write(traceback.format_exc())
    global lcd
    global error_incident_flag
    error_incident_flag += 1
    lcd.clear()
    gpio.cleanup()


def displayIP():
    global lcd
    lcd.clear()
    ip_address = os.popen('hostname -I').read()
    lcd.message(str(ip_address))
    print('\nDisplaying IP...')


def restartPrep():
    os.popen('pkill chromium')
    global outfile
    global error_incident_flag
    if error_incident_flag != 0:
        new_outfile = outfile + '%' + str(error_incident_flag)
        os.rename(outfile, new_outfile)
        with open(outfile, 'a') as f:
            restart_time = datetime.now().strftime("%H %M %S")
            f.write(f'\nSession restarted at {restart_time} with {error_incident_flag} error(s).')
    else:
        with open(outfile, 'a') as f:
            restart_time = datetime.now().strftime("%H %M %S")
            f.write(f'\nSession restarted at {restart_time} with no errors.')
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
            if (the_date in name) and ('hourly_log' in name) and ('%' not in name):
                print(f'clean hourly log found: {name}')
                os.remove(f'sesson_logs/{name}')
            else:
                error_logs.append(name)

    sorted(error_logs)
    outfile = f'session_logs/daily_log_{the_date}'
    with open(outfile, 'a') as f:
        f.write(f'\nDay: {the_date}')
        f.write(f'\nDay completed with {error_incident_flag} error(s).')
        f.write('\nErrors:\n\n')
        for log in error_logs:
            f.write(f'In: {log}:\n')
            lines = f.readlines(log)
            f.write(lines)
            f.write('\n')
        f.write(f'\nLog entered at {datetime.now.strftime("%Y-%m-%d: %H:%M:%S")}')

