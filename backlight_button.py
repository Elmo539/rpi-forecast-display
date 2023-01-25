import RPi.GPIO as gpio
from time import sleep


def dark_button(parameter):
    print('dark_button pressed with parameter', parameter)
    swap = {0:1, 1:0}

    global lcd_light_flag
    lcd_light_flag = swap[lcd_light_flag]

    if lcd_light_flag == 0:
        print("button=0")
        gpio.output(10, False)
    elif lcd_light_flag == 1:
        print("button=1")
        gpio.output(10, True)
    else:
        pass

    return lcd_light_flag

def main():
    gpio.setmode(gpio.BCM)

    global lcd_light_flag
    lcd_light_flag = 0

    gpio.setup(10, gpio.OUT)
    gpio.output(10, True)

    button_pin = 9
    gpio.setup(button_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.add_event_detect(button_pin, gpio.BOTH, callback=dark_button, bouncetime=400)

    try:
        while True:
            print("Monitoring button...")
            sleep(10)
    except KeyboardInterrupt:
        gpio.remove_event_detect(button_pin)
        gpio.cleanup()


if __name__ == '__main__':
    main()

