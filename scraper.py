from selenium import webdriver
import json
from datetime import datetime
import time
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key, Controller
baseUrl = 'https://www.transfermarkt.com'



countryCompleted = False
competitionCompleted = False
clubCompleted = False
playerCompleted = False

countryBreakPoint = 0
competitionBreakPoint = 0
clubBreakPoint = 0
playerBreakPoint = 0

def parser(countryStart, competitionStart, clubStart, playerStart):
    options = webdriver.FirefoxOptions()
    #options.add_argument('-headless')
    global driver
    driver = webdriver.Firefox(executable_path="/home/toor/Desktop/firefoxGeckoDriver/geckodriver", firefox_options=options)
    keyboard = Controller()
    keyboard.press(Key.cmd)
    keyboard.press(Key.right)
    keyboard.release(Key.cmd)
    keyboard.release(Key.right)
    driver.get(baseUrl)

    countryDropDownMenu = driver.find_element_by_id('land_select_breadcrumb_chzn')
    countryDropDownMenu.click()
    time.sleep(3)
    allCountriesList = driver.find_elements_by_class_name('active-result')

    for countryNumber in range(countryStart, len(allCountriesList)):
        country = allCountriesList[countryNumber]
        global countryBreakPoint
        countryBreakPoint = countryNumber
        countryName = country.text
        print(countryName)
        country.click()

        country_enter_button = driver.find_element_by_class_name('breadcrumb-button')
        country_enter_button.click()
        time.sleep(1)

        responsiveDiv = driver.find_elements_by_class_name('responsive-table')
        allCompetitionListTable = responsiveDiv[0].find_elements_by_class_name('inline-table')

        for competitionNumber in range(competitionStart, len(allCompetitionListTable)):
            global competitionBreakPoint
            competitionBreakPoint = competitionNumber
            allTdsForCompetitionLinks = allCompetitionListTable[competitionNumber].find_elements_by_tag_name("td")

            competitionName = allTdsForCompetitionLinks[1].text
            print("\t" + str(competitionName).strip('\n'))
            allTdsForCompetitionLinks[1].click()

            competitionBreakPoint = 0
            allClubLinks = driver.find_elements_by_class_name('hauptlink.no-border-links.show-for-small.show-for-pad')

            for clubNumber in range(clubStart, len(allClubLinks)):
                teamsJson = open('teams.json', 'a')
                keyboard.press(Key.down)
                time.sleep(1)
                keyboard.release(Key.down)
                global clubBreakPoint
                clubBreakPoint = clubNumber
                clubNameAndLink = allClubLinks[clubNumber].find_element_by_class_name('vereinprofil_tooltip.tooltipstered')
                clubName = clubNameAndLink.text

                print("\t\t" + str(clubNumber) + ": " + clubName)
                global clubCompleted

                clubNameAndLink.click()
                if clubCompleted is False:
                    clubDict = {}
                    clubDict['club_name'] = clubName
                    clubDict['club_country'] = countryName
                    clubDict['competition_name'] = competitionName
                    clubDict['updated_date'] = str(datetime.now())

                    clubValueField = driver.find_element_by_class_name('dataMarktwert')
                    clubValue = clubValueField.find_element_by_css_selector('a').text
                    clubValue += " " + clubValueField.find_element_by_class_name('waehrung').text
                    clubDict['total_value'] = clubValue[:clubValue.index("€") + 1]

                    json.dump(clubDict, teamsJson, indent=4, ensure_ascii=False)
                    teamsJson.write(',')
                    teamsJson.close()
                clubCompleted = True
                allPlayerLinks = driver.find_elements_by_class_name('posrela')
                currentClubUrl = driver.current_url

                for playerNumber in range(playerStart, len(allPlayerLinks)):
                    playersJson = open('players.json', 'a')
                    global playerBreakPoint
                    playerBreakPoint = playerNumber
                    playerClickFlag = False
                    try:
                        playerNameAndLink = allPlayerLinks[playerNumber].find_element_by_class_name('spielprofil_tooltip.tooltipstered')
                        playerName = playerNameAndLink.text
                        print("\t\t\t" + str(playerNumber) + ": " + playerName)
                        playerNameAndLink.click()
                        playerClickFlag = True

                        player_stats_all = driver.find_elements_by_class_name('auflistung')

                        player_stats_main = player_stats_all[2]
                        player_bdate = ""
                        player_nation = ""
                        player_position = ""

                        for stat in player_stats_main.find_elements_by_tag_name('tr'):
                            clean_info = stat.find_element_by_tag_name('td')

                            if (stat.find_element_by_tag_name('th').text.strip() == 'Date of birth:'):
                                player_bdate = clean_info.text.strip()
                            elif (stat.find_element_by_tag_name('th').text.strip() == 'Nationality:'):
                                player_nation = clean_info.text.strip()
                            elif (stat.find_element_by_tag_name('th').text.strip() == 'Position:'):
                                player_position = clean_info.text.strip()

                        playerDict = {}
                        playerDict['name'] = playerName
                        playerDict['date_of_birth'] = player_bdate
                        playerDict['nationality'] = player_nation
                        playerDict['position'] = player_position
                        playerDict['current_club'] = clubName
                        playerDict['price'] = ""
                        playerDict['updated_date'] = str(datetime.now())

                        json.dump(playerDict, playersJson, indent=4, ensure_ascii=False)
                        playersJson.write(',')
                        playersJson.close()

                    except:
                        print("player parse error")

                    if playerClickFlag is True:
                        driver.get(currentClubUrl)
                        time.sleep(1)
                    allPlayerLinks = driver.find_elements_by_class_name('posrela')
                    playerBreakPoint = 0
                    playerStart = 0

                    logTxt = open('log.txt', 'a')
                    logTxt.write('\n')
                    logTxt.write(':' + str(countryNumber) + "," + str(competitionNumber) + "," + str(clubNumber) + "," + str(playerNumber) + "\n")
                    logTxt.close()

                clubCompleted = False
                #repeat steps for other clubs
                clubBreakPoint = 0
                clubStart = 0
                driver.back()
                allClubLinks = driver.find_elements_by_class_name('hauptlink.no-border-links.show-for-small.show-for-pad')

            #repeat steps for other competitions
            countryBreakPoint = 0
            driver.back()
            responsiveDiv = driver.find_elements_by_class_name('responsive-table')
            allCompetitionListTable = responsiveDiv[0].find_elements_by_class_name('inline-table')

        #repeat steps for other countries
        countryDropDownMenu = driver.find_element_by_id('land_select_breadcrumb_chzn')
        countryDropDownMenu.click()
        time.sleep(1)
        allCountriesList = driver.find_elements_by_class_name('active-result')

if(__name__ == '__main__'):
    with open('log.txt', 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
        resumeNumbers = last_line[1:].split(',')

    if len(resumeNumbers) == 4:
        countryBreakPoint = int(resumeNumbers[0])
        competitionBreakPoint = int(resumeNumbers[1])
        clubBreakPoint = int(resumeNumbers[2])
        playerBreakPoint = int(resumeNumbers[3])
        countryCompleted = True
        competitionCompleted = True
        clubCompleted = True

    while True:
        try:
            parser(countryBreakPoint, competitionBreakPoint, clubBreakPoint, playerBreakPoint)
            break
        except Exception as e:
            print(str(e))
            globals().get('driver').close()
            pass
