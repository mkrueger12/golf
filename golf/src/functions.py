import requests
import pandas as pd
import time
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_user_key():
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    # Create the webdriver object and pass the arguments
    options = webdriver.ChromeOptions()

    # Chrome will start in Headless mode
    options.add_argument('headless')

    # Ignores any certificate errors if there is any
    options.add_argument("--ignore-certificate-errors")

    # Startup the chrome webdriver with executable path and
    # pass the chrome options and desired capabilities as
    # parameters.
    print('building driver')
    driver = webdriver.Chrome(
        executable_path="/Users/maxwellkrueger/Documents/PythonProjects/golf/project/bin/chromedriver",
        chrome_options=options,
        desired_capabilities=desired_capabilities)
    # Send a request to the website and let it load
    driver.get('https://www.pgatour.com/players/player.28237.rory-mcilroy.html')

    # Sleeps for 10 seconds
    #time.sleep(10)

    # Gets all the logs from performance in Chrome
    print('getting logs')
    logs = driver.get_log("performance")

    for i in range(len(logs)):
        log = json.loads(logs[i]['message'])

        try:
            type = log['message']['params']['type']
            print(i, type, log['message']['method'])
        except KeyError:
            print('KeyError')
            continue

        if (type == 'XHR') & (log['message']['method'] == 'Network.requestWillBeSent'):
            if len(log['message']['params']['request']['url']) > 75:

                print(log['message']['params']['request']['url'])

                try:
                    userKey = log['message']['params']['request']['url'].split('&')[3]

                    userKey = userKey.replace('userTrackingId=', '')
                    print('userkey found')

                    driver.quit()

                    return userKey
                except IndexError:
                    print('IndexError')
                    continue
