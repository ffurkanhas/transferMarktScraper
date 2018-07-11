from selenium import webdriver
import json
from datetime import datetime
import time
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key, Controller
baseUrl = 'https://www.transfermarkt.com'

playersJson = open('players.json', 'a')
teamsJson = open('teams.json', 'a')
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
        countryStart = 0
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
            competitionStart = 0
            global competitionBreakPoint
            competitionBreakPoint = competitionNumber
            allTdsForCompetitionLinks = allCompetitionListTable[competitionNumber].find_elements_by_tag_name("td")

            competitionName = allTdsForCompetitionLinks[1].text
            print("\t" + str(competitionName).strip('\n'))
            allTdsForCompetitionLinks[1].click()
            allClubLinks = driver.find_elements_by_class_name('hauptlink.no-border-links.show-for-small.show-for-pad')

            for clubNumber in range(clubStart, len(allClubLinks)):
                clubStart = 0
                global clubBreakPoint
                clubBreakPoint = clubNumber
                clubNameAndLink = allClubLinks[clubNumber].find_element_by_class_name('vereinprofil_tooltip.tooltipstered')
                clubName = clubNameAndLink.text
                print("\t" + str(clubNumber) + ": " + clubName)
                clubNameAndLink.click()

                allPlayerLinks = driver.find_elements_by_class_name('posrela')

                for playerNumber in range(playerStart, len(allPlayerLinks)):
                    playerStart = 0
                    global playerBreakPoint
                    playerBreakPoint = playerNumber
                    playerNameAndLink = allPlayerLinks[playerNumber].find_element_by_class_name('spielprofil_tooltip.tooltipstered')
                    playerName = playerNameAndLink.text
                    print("\t\t" + str(playerNumber) + ": " + playerName)
                    playerNameAndLink.click()

                    #repeat steps for other players
                    driver.back()
                    allPlayerLinks = driver.find_elements_by_class_name('posrela')

                #repeat steps for other clubs
                driver.back()
                allClubLinks = driver.find_elements_by_class_name('hauptlink.no-border-links.show-for-small.show-for-pad')

            #repeat steps for other competitions
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
    # allTdsForClubLinks = driver.find_elements_by_class_name('hauptlink no-border-links hide-for-small hide-for-pad')
    #
    # for clubNumber in range(0, len(allTdsForClubLinks)):
    #     clubNameAndLink = allTdsForClubLinks[clubNumber].find_element_by_class_name(
    #         'vereinprofil_tooltip tooltipstered')
    #     clubName = clubNameAndLink.text
    #     print(clubName)
    #     clubNameAndLink.click()