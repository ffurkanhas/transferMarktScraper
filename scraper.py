from selenium import webdriver
import json
from datetime import datetime
import time
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key, Controller
baseUrl = 'https://www.transfermarkt.com'

logTxt = open('log.txt', 'a')

countryCompleted = False
competitionCompleted = False
clubCompleted = False
playerCompleted = False

countryBreakPoint = 1
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
                global clubBreakPoint
                clubBreakPoint = clubNumber
                clubNameAndLink = allClubLinks[clubNumber].find_element_by_class_name('vereinprofil_tooltip.tooltipstered')
                clubName = clubNameAndLink.text

                print("\t" + str(clubNumber) + ": " + clubName)
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

                for playerNumber in range(playerStart, len(allPlayerLinks)):
                    playersJson = open('players.json', 'a')
                    global playerBreakPoint
                    playerBreakPoint = playerNumber
                    playerNameAndLink = allPlayerLinks[playerNumber].find_element_by_class_name('spielprofil_tooltip.tooltipstered')
                    playerName = playerNameAndLink.text
                    print("\t\t" + str(playerNumber) + ": " + playerName)

                    playersJson.close()
                    playerNameAndLink.click()

                    #repeat steps for other players
                    playerBreakPoint = 0
                    playerStart = 0
                    driver.back()
                    allPlayerLinks = driver.find_elements_by_class_name('posrela')

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
        logTxt.write('Country: ' + str(countryNumber) + "\n")
        countryDropDownMenu = driver.find_element_by_id('land_select_breadcrumb_chzn')
        countryDropDownMenu.click()
        time.sleep(1)
        allCountriesList = driver.find_elements_by_class_name('active-result')

if(__name__ == '__main__'):
    logTxt.write('\n----------------\n' + str(datetime.now()))
    while True:
        try:
            parser(countryBreakPoint, competitionBreakPoint, clubBreakPoint, playerBreakPoint)
            break
        except Exception as e:
            print(str(e))
            globals().get('driver').close()
            pass
    logTxt.close()
