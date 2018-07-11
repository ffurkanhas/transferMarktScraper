from selenium import webdriver
import json
from datetime import datetime
import time
from selenium.webdriver.common.keys import Keys
baseUrl = 'https://www.transfermarkt.com'

playersJson = open('players.json', 'a')
teamsJson = open('teams.json', 'a')
logTxt = open('log.txt', 'a')

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
    driver.maximize_window()

    driver.get(baseUrl)
    time.sleep(3)

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
            time.sleep(2)
            allClubLinks = driver.find_elements_by_class_name('hauptlink.no-border-links.show-for-small.show-for-pad')

            for clubNumber in range(clubStart, len(allClubLinks)):
                global clubBreakPoint
                clubBreakPoint = clubNumber
                time.sleep(3)
                clubNameAndLink = allClubLinks[clubNumber].find_element_by_class_name('vereinprofil_tooltip.tooltipstered')
                print("ok")
                time.sleep(2)
                clubName = clubNameAndLink.text
                print("\t" + str(clubNumber) + ": " + clubName)
                clubNameAndLink.click()


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
    # while True:
    #     try:
    #
    #         break
    #     except Exception as e:
    #         print(str(e))
    #         globals().get('driver').close()
    #         pass
    parser(countryBreakPoint, competitionBreakPoint, clubBreakPoint, playerBreakPoint)
    logTxt.close()
    # allTdsForClubLinks = driver.find_elements_by_class_name('hauptlink no-border-links hide-for-small hide-for-pad')
    #
    # for clubNumber in range(0, len(allTdsForClubLinks)):
    #     clubNameAndLink = allTdsForClubLinks[clubNumber].find_element_by_class_name(
    #         'vereinprofil_tooltip tooltipstered')
    #     clubName = clubNameAndLink.text
    #     print(clubName)
    #     clubNameAndLink.click()