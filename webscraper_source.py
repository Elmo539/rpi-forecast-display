"""
TO DO NEXT:
    - add manual click-through functionality
    \ fix bad url handling
    - finish commenting
"""

import traceback
import pprint
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_experimental_option('detach', True)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('start-maximized')

print("\nwebscraper ready")

path = Service("/usr/lib/chromium-browser/chromedriver")
driver = webdriver.Chrome(service=path, options=options)
try:
    driver.get('https://forecast.weather.gov/MapClick.php?lat=38.895&lon=-77.0373&lg=english&FcstType=digital')
except Exception:
    with open('log.txt', 'a') as f:
        f.write('\n' + str(datetime.now()) + '::\n')
        f.write('Error in finding webscraper url\n')
        f.write(traceback.format_exc())

def getHours():
    hour_row = driver.find_elements(By.XPATH, "/html/body/table[6]/tbody/tr[3]/td")
    global hours
    hours = []
    for hour in range(17):
        hours.append(hour_row[hour].text)


def getTemps():
    temp_row = driver.find_elements(By.XPATH, "/html/body/table[6]/tbody/tr[4]/td")
    global temps
    temps = []
    for temp in range(len(hours)):
        temps.append(temp_row[temp].text)


def getDewpoints():
    dewpoint_row = driver.find_elements(By.XPATH, "/html/body/table[6]/tbody/tr[5]/td")
    global dewpoints
    dewpoints = []
    for point in range(len(hours)):
        dewpoints.append(dewpoint_row[point].text)


def getWinds():
    wind_row = driver.find_elements(By.XPATH, "/html/body/table[6]/tbody/tr[7]/td")
    global winds
    winds = []
    for wind in range(len(hours)):
        winds.append(wind_row[wind].text)


def getSkyCover():
    sky_cover_row = driver.find_elements(By.XPATH, "/html/body/table[6]/tbody/tr[10]/td")
    global sky_covers
    sky_covers = []
    for sky_cover in range(len(hours)):
        sky_covers.append(sky_cover_row[sky_cover].text)


def getPrecip():
    precip_row = driver.find_elements(By.XPATH, "/html/body/table[6]/tbody/tr[11]/td")
    global precips
    precips = []
    for precip in range(len(hours)):
        precips.append(precip_row[precip].text)


global placeholder
placeholder = []

global template_dict
template_dict = {'topic': '', 'data': placeholder, 'max': placeholder, 'min': placeholder}


def findMax(thelist):
    try:
        list_max = thelist[0]
        for i in thelist:
            if i > list_max:
                list_max = i
        return list_max
    except IndexError:
        print("IndexError in findMax()")
        list_max = 'na'
        return list_max


def findMin(thelist):
    try:
        list_min = thelist[0]
        for i in thelist:
            if i < list_min:
                list_min = i
        return list_min
    except IndexError:
        list_min = 'na'
        return list_min


def getTodaysHours():
    global just_hours
    just_hours = []
    hours_dict = {'topic': '', 'data': placeholder, 'max': placeholder, 'min': placeholder}

    for hour in hours:
        if len(hour) == 2:
            just_hours.append(int(hour))
        else:
            hours_dict['topic'] = hour
    hours_dict['data'] = just_hours
    hours_dict['max'] = findMax(just_hours)
    hours_dict['min'] = findMin(just_hours)
    return hours_dict


def getTodaysTemps():
    just_temps = []
    temps_dict = {'topic': '', 'data': placeholder, 'max': placeholder, 'min': placeholder}

    for temp in temps:
        if len(temp) == 2:
            just_temps.append(int(temp))
        else:
            temps_dict['topic'] = temp
    temps_dict['data'] = just_temps
    temps_dict['max'] = findMax(just_temps)
    temps_dict['min'] = findMin(just_temps)
    return temps_dict


def getTodaysDewpoints():
    just_dewpoints = []
    dewpoints_dict = {'topic': '', 'data': placeholder, 'max': placeholder, 'min': placeholder}

    for dp in dewpoints:
        if len(dp) == 2:
            just_dewpoints.append(int(dp))
        else:
            dewpoints_dict['topic'] = dp
    dewpoints_dict['data'] = just_dewpoints
    dewpoints_dict['max'] = findMax(just_dewpoints)
    dewpoints_dict['min'] = findMin(just_dewpoints)
    return dewpoints_dict


def getTodaysWinds():
    just_winds = []
    winds_dict = {'topic': '', 'data': placeholder, 'max': placeholder, 'min': placeholder}

    for wind in winds:
        if len(wind) <= 2:
            just_winds.append(int(wind))
        else:
            winds_dict['topic'] = wind
    winds_dict['data'] = just_winds
    winds_dict['max'] = findMax(just_winds)
    winds_dict['min'] = findMin(just_winds)
    return winds_dict


def getTodaysSkyCover():
    just_sky_covers = []
    sky_covers_dict = {'topic': '', 'data': placeholder, 'max': placeholder, 'min': placeholder}

    for sky_cover in sky_covers:
        if len(sky_cover) == 2:
            just_sky_covers.append(int(sky_cover))
        else:
            sky_covers_dict['topic'] = sky_cover
    sky_covers_dict['data'] = just_sky_covers
    sky_covers_dict['max'] = findMax(just_sky_covers)
    sky_covers_dict['min'] = findMin(just_sky_covers)
    return sky_covers_dict


def getTodaysPrecip():
    just_precips = []
    precips_dict = {'topic': '', 'data': placeholder, 'max': placeholder, 'min': placeholder}

    for precip in precips:
        if len(precip) <= 3:
            just_precips.append(int(precip))
        else:
            precips_dict['topic'] = precip
    precips_dict['data'] = just_precips
    precips_dict['max'] = findMax(just_precips)
    precips_dict['min'] = findMin(just_precips)
    return precips_dict


def main():
    print("\nwebscraper running")

    driver.refresh()

    export_packet = {}

    try:
        getHours()
        getTemps()
        getDewpoints()
        getWinds()
        getSkyCover()
        getPrecip()

    except Exception:
        with open('log.txt', 'a') as f:
            f.write('\n' + str(datetime.now()) + '::\n')
            f.write('Error in webscraper_source.main()\n')
            f.write(traceback.format_exc())
        return

    fin_hours = getTodaysHours()
    export_packet['hours'] = fin_hours

    fin_temps = getTodaysTemps()
    export_packet['temps'] = fin_temps

    fin_dewpoints = getTodaysDewpoints()
    export_packet['dewpoints'] = fin_dewpoints

    fin_winds = getTodaysWinds()
    export_packet['winds'] = fin_winds

    fin_skycover = getTodaysSkyCover()
    export_packet['skycover'] = fin_skycover

    fin_precip = getTodaysPrecip()
    export_packet['precip'] = fin_precip


    #pprint.pprint(export_packet, width=55, sort_dicts=False)
    print("\nData loaded.\nExporting packet...")
    return export_packet

if __name__ == "__main__":
    main()

