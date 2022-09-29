import requests
import pandas as pd
import time
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# get players table
url = 'https://statdata.pgatour.com/players/player.json?userTrackingId=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjQxNDIxOTEsIm5iZiI6MTY2NDE0MjE5MSwiZXhwIjoxNjY0MTQzOTkxfQ.tiBDggyR7nuPki_ZcexFhMD-AKZZy7friUqI_ZS8zpQ'

df = requests.get(url).json()
players = pd.DataFrame(df['plrs'])

# course history url
#https://statdata-api-prod.pgatour.com/api/clientfile/PlayerCourseResults?P_ID=28237&T_CODE=r&format=json&userTrackingId=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjQxNDIxOTEsIm5iZiI6MTY2NDE0MjE5MSwiZXhwIjoxNjY0MTQzOTkxfQ.tiBDggyR7nuPki_ZcexFhMD-AKZZy7friUqI_ZS8zpQ
#tournament history
#https://statdata-api-prod.pgatour.com/api/clientfile/PlayerTournamentHistoryRef?P_ID=28237&format=json&userTrackingId=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjQxNDIxOTEsIm5iZiI6MTY2NDE0MjE5MSwiZXhwIjoxNjY0MTQzOTkxfQ.tiBDggyR7nuPki_ZcexFhMD-AKZZy7friUqI_ZS8zpQ

# tournament list
#https://www.pgatour.com/content/dam/pgatour/system/weather-tournaments-sponsors.json
#https://statdata-api-prod.pgatour.com/api/clientfile/schedule-v2?format=json&userTrackingId=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjQzODU2MTQsIm5iZiI6MTY2NDM4NTYxNCwiZXhwIjoxNjY0Mzg3NDE0fQ.XlpVqPN1OcJ47cGfcC2xibM9g4czQz_LP7rHDEaJkU4

#weather data
#https://www.pgatour.com/bin/data/feeds/weather.json/r464

#leaderboard
#https://statdata.pgatour.com/r/054/leaderboard-v2mini.json?userTrackingId=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjQzODU2MTQsIm5iZiI6MTY2NDM4NTYxNCwiZXhwIjoxNjY0Mzg3NDE0fQ.XlpVqPN1OcJ47cGfcC2xibM9g4czQz_LP7rHDEaJkU4


#twitter feed
#https://api.massrelevance.com/brgyan07p/tournament_r054.json

#player stats
#https://statdata.pgatour.com/r/521/2022/player_stats.json?userTrackingId=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjQzODY1NDAsIm5iZiI6MTY2NDM4NjU0MCwiZXhwIjoxNjY0Mzg4MzQwfQ.GQA5_XVCkiY_G4C_CPTdGg8eIsWpsIGeFLWFHZ7xVh0

# shot data
#https://statdata.pgatour.com/r/521/2022/scorecards/28237.json?userTrackingId=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjQ0MTMzMTEsIm5iZiI6MTY2NDQxMzMxMSwiZXhwIjoxNjY0NDE1MTExfQ.AxpCVHEnoaWCtUr8yveE5Jg3uI-2Reb_nUvhvk4_ueg

#get userKey

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
driver = webdriver.Chrome(executable_path="/Users/maxwellkrueger/Documents/PythonProjects/golf/project/bin/chromedriver",
                          chrome_options=options,
                          desired_capabilities=desired_capabilities)
# Send a request to the website and let it load
driver.get('https://www.pgatour.com/players/player.28237.rory-mcilroy.html/scorecards/r521')

# Sleeps for 10 seconds
#time.sleep(10)

# Gets all the logs from performance in Chrome
logs = driver.get_log("performance")
log = json.loads(logs[0]['message'])
type = log['message']['params']['type']
userKey = log['message']['params']['request']['url'].split('&')[3]
userKey = userKey.replace('userTrackingId=', '')



driver.quit()
# get player stats
url = 'https://statdata.pgatour.com/r/060/2022/scorecards/28237.json?userTrackingId=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjQxNDIxOTEsIm5iZiI6MTY2NDE0MjE5MSwiZXhwIjoxNjY0MTQzOTkxfQ.tiBDggyR7nuPki_ZcexFhMD-AKZZy7friUqI_ZS8zpQ'
stats = requests.get(url).json()
rnds = []

for i in range(len(stats['p']['rnds'])):
    holes = pd.DataFrame(stats['p']['rnds'][i]['holes'])
    holes['rnd'] = i + 1
    rnds.append(holes)

rnds = pd.concat(rnds)

# get tournament list
url = 'https://statdata.pgatour.com/r/521/2022/player_stats.json?userTrackingId=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjQzODY1NDAsIm5iZiI6MTY2NDM4NjU0MCwiZXhwIjoxNjY0Mzg4MzQwfQ.GQA5_XVCkiY_G4C_CPTdGg8eIsWpsIGeFLWFHZ7xVh0
stats = requests.get(url).json()
rnds = []

for i in range(0,1000):
    i = str(i).zfill(3)
    url = f'https://statdata.pgatour.com/r/{i}/2022/player_stats.json?userTrackingId=eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjQ0MTA4MTIsIm5iZiI6MTY2NDQxMDgxMiwiZXhwIjoxNjY0NDEyNjEyfQ.zeLAzOuhL0NapJ_1GafwjaXS4sfSZaxlub49aF1-_uM'
    response = requests.get(url).status_code
    if response == 200:
        print(i, response)
        data = {'tournament': i, 'status': response}
        rnds.append(data)
    else:
        pass

rnds = pd.DataFrame(rnds)
rnds.to_csv('golf/data/external/pga_tour_tournaments.csv')



# get shot data
for y in range(2018, 2023):
    id = get_user_key()

    for t in tournaments:
        data = []
        t = str(t).zfill(3)

        for p in players:
            url = f'https://statdata.pgatour.com/r/{t}/{y}/scorecards/{p}.json?userTrackingId={id}'
            print(requests.get(url).status_code, url)

            if requests.get(url).status_code == 200:

                r = requests.get(url).content
                r = json.loads(r)

                for i in range(len(r['p']['rnds'])):
                    df = pd.json_normalize(r['p']['rnds'][0], ['holes', ['shots']], max_level=1)

                    df['round'] = i + 1
                    df['tournament'] = t
                    df['year'] = y

                    data.append(df)

        data = pd.concat(data)
        data.to_csv(f'golf/data/interim/{y}_{t}.csv', index=False)
