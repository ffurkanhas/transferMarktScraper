from selenium import webdriver
import json
from datetime import datetime
import time
from pynput.keyboard import Key, Controller
import os.path

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
            competitionsJson = open('competitions.json', 'a')
            global competitionBreakPoint
            global competitionCompleted
            competitionBreakPoint = competitionNumber
            allTdsForCompetitionLinks = allCompetitionListTable[competitionNumber].find_elements_by_tag_name("td")

            competitionName = allTdsForCompetitionLinks[1].text
            print("\t" + str(competitionName).strip('\n'))
            allTdsForCompetitionLinks[1].click()

            competitionBreakPoint = 0

            competitionValue = ""

            if 'box-content' in driver.page_source:
                tempBoxContent = driver.find_element_by_class_name('box-content')
                if 'marktwert' in tempBoxContent.get_attribute('innerHTML'):
                    competitionValueField = tempBoxContent.find_element_by_class_name('marktwert')
                    competitionValue = competitionValueField.find_element_by_css_selector('a').text
                    print("Competition Value: " + competitionValue)

            if competitionCompleted is False:
                competitionDict = {}
                competitionDict['name'] = competitionName
                competitionDict['total_value'] = competitionValue

                json.dump(competitionDict, competitionsJson, indent=4, ensure_ascii=False)
                competitionsJson.write(',')
                competitionsJson.close()

            competitionCompleted = True

            allClubLinks = driver.find_elements_by_class_name('hauptlink.no-border-links.show-for-small.show-for-pad')

            for clubNumber in range(clubStart, len(allClubLinks)):
                teamsJson = open('teams.json', 'a')
                keyboard.press(Key.down)
                time.sleep(0.5)
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

                    if 'dataMarktwert' in driver.page_source:
                        clubValueField = driver.find_element_by_class_name('dataMarktwert')
                        clubValue = clubValueField.find_element_by_css_selector('a').text
                        clubValue += " " + clubValueField.find_element_by_class_name('waehrung').text
                        clubDict['total_value'] = clubValue[:clubValue.index("€") + 1]
                    else:
                        clubDict['total_value'] = ""

                    json.dump(clubDict, teamsJson, indent=4, ensure_ascii=False)
                    teamsJson.write(',')
                    teamsJson.close()
                clubCompleted = True
                allPlayerLinks = driver.find_elements_by_class_name('posrela')
                currentClubUrl = driver.current_url

                for playerNumber in range(playerStart, len(allPlayerLinks)):
                    if not os.path.isfile("./datas/" + competitionName + '.json'):
                        with open("./datas/" +competitionName + '.json', 'a') as file:
                            file.write("[")
                            file.close()

                    playersJson = open("./datas/" + competitionName + '.json', 'a')
                    global playerBreakPoint
                    playerBreakPoint = playerNumber
                    playerClickFlag = False
                    try:
                        playerNameAndLink = allPlayerLinks[playerNumber].find_element_by_class_name('spielprofil_tooltip')
                        playerName = playerNameAndLink.text
                        print("\t\t\t" + str(playerNumber) + ": " + playerName)
                        playerNameAndLink.click()
                        playerClickFlag = True

                        player_stats_all = driver.find_element_by_class_name('spielerdaten')
                        player_stats_all = player_stats_all.find_element_by_class_name('auflistung')

                        player_stats_main = player_stats_all
                        player_bdate = ""
                        player_nation = ""
                        player_position = ""

                        for stat in player_stats_main.find_elements_by_tag_name('tr'):
                            clean_info = stat.find_element_by_tag_name('td')

                            if (stat.find_element_by_tag_name('th').text.strip() == 'Date of Birth:'):
                                player_bdate = clean_info.text.strip()
                            elif (stat.find_element_by_tag_name('th').text.strip() == 'Nationality:'):
                                player_nation = clean_info.text.strip()
                            elif (stat.find_element_by_tag_name('th').text.strip() == 'Position:'):
                                player_position = clean_info.text.strip()

                        playerDict = {}

                        if 'dataMarktwert' in driver.page_source:
                            playerValueField = driver.find_element_by_class_name('dataMarktwert')
                            playerValue = playerValueField.find_element_by_css_selector('a').text
                            playerValue += " " + playerValueField.find_element_by_class_name('waehrung').text
                            playerValue = playerValue[:playerValue.index("€") + 1]
                            playerDict['value'] = playerValue
                        else:
                            playerDict['value'] = ""

                        playerDict['name'] = playerName
                        playerDict['date_of_birth'] = player_bdate
                        playerDict['nationality'] = player_nation
                        playerDict['position'] = player_position
                        playerDict['current_club'] = clubName
                        playerDict['updated_date'] = str(datetime.now())
                        playerDict['player_index'] = str(countryNumber) + ", " + str(competitionNumber) + ", " + str(clubNumber) + ", " + str(playerNumber)

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
                    logTxt.write(':' + str(countryNumber) + "," + str(competitionNumber) + "," + str(clubNumber) + "," + str(playerNumber) + "\n")
                    logTxt.close()

                clubCompleted = False
                #repeat steps for other clubs
                clubBreakPoint = 0
                clubStart = 0
                driver.back()
                allClubLinks = driver.find_elements_by_class_name('hauptlink.no-border-links.show-for-small.show-for-pad')

            with open("./datas/" + competitionName + '.json', 'a') as file:
                file.write("{}]")
                file.close()

            competitionCompleted = False
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
        if (lines):
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
