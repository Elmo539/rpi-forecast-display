# rpi-forecast-display

This is the code for a weather forecast display I made using a RaspberryPi 3b and a 16x2 LCD display (non-I^2^C).
The goal of this project was to automate checking the weather forecast, especially in the mornings when many of us are particularly lazy.
## Resources
The data was webscraped from the [National Weather Service's](https://forecast.weather.gov/MapClick.php?lat=38.895&lon=-77.0373&unit=0&lg=english&FcstType=digital) website, specifically the Washington, D.C. forecast.
I used [Selenium](https://www.selenium.dev/documentation/) as my webscraping tool.
As far as the hardware goes, I used the [Adafruit_CharLCD](https://github.com/adafruit/Adafruit_Python_CharLCD) library for controlling the LCD, which has since been deprecated so it may not be a good idea to use.
I also used the [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) library for RaspberryPi control.
Additionally, I am running it headless. You may notice some `print()` statements throughout; that is only for development purposes.
## Extra stuff
The headless nature and goal of automation of this project required me to add a lot of extra code throughout the project which some might deem unnecessary for their purposes.
This is the first time that I am seriously grappling with Linux. This, coupled with the goal of automation, has forced me to learn a lot about Linux and there are several additional bits of code spread around my OS that aren't present in this repo, such as automatic network connectivity, static IP addresses for SSH, and some very primitve bash scripting in the autostart folder that I will most certainly NOT be showing.
This project is still being refined, so if you have any suggestions be sure to let me know!
