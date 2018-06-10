from selenium import webdriver
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
display.start()

baseUrl = 'https://www.transfermarkt.com'

countryBreakPoint = 0
competitionBreakPoint = 0
clubBreakPoint = 0
playerBreakPoint = 0

isCountryCompleted = False
isCompetitionCompleted = False
isClubCompleted = False
isPlayerCompleted = False

def parser(countryStart, competionStart, clubStart, playerStart):
  global isCountryCompleted, isCompetitionCompleted, isClubCompleted, isPlayerCompleted

  options = webdriver.FirefoxOptions()
  options.add_argument('-headless')
  global driver
  driver = webdriver.Firefox(firefox_options=options)

  driver.get(baseUrl)

  countryMenu = driver.find_element_by_id('land_select_breadcrumb_chzn')
  countryMenu.click()

  allCountries = driver.find_elements_by_class_name('active-result')

  for country in range(countryStart, len(allCountries)):
    isCountryCompleted = False

    global countryBreakPoint
    countryBreakPoint = country
    country = allCountries[country]
    countryName = country.text

    print(countryName)

    country.click()

    competitionMenu = driver.find_element_by_id('wettbewerb_select_breadcrumb_chzn')
    competitionMenu.click()

    allCompetitions = competitionMenu.find_elements_by_class_name('active-result')

    if len(allCompetitions) > 1:

      for competition in range(competionStart, len(allCompetitions)):
        isCompetitionCompleted = False

        global competitionBreakPoint
        competitionBreakPoint = competition
        competition = allCompetitions[competition]
        competitionName = competition.text

        print("\t" + competitionName)

        competition.click()

        clubMenu = driver.find_element_by_id('verein_select_breadcrumb_chzn')
        clubMenu.click()

        allClubs = clubMenu.find_elements_by_class_name('active-result')

        for club in range(clubStart, len(allClubs)):
          isClubCompleted = False

          global clubBreakPoint
          clubBreakPoint = club
          club = allClubs[club]
          clubName = club.text

          print("\t\t" + clubName)

          club.click()

          playerMenu = driver.find_element_by_id('spieler_select_breadcrumb_chzn')
          playerMenu.click()

          allPlayers = playerMenu.find_elements_by_class_name('active-result')

          for player in range(playerStart, len(allPlayers)):
            isPlayerCompleted = False

            global playerBreakPoint
            playerBreakPoint = player
            player = allPlayers[player]
            playerName = player.text

            print("\t\t\t" + playerName)

            player.click()

            playerSubmitButton = driver.find_elements_by_class_name('breadcrumb-button')
            playerSubmitButton[3].click()

            isPlayerCompleted = True

            playerMenu = driver.find_element_by_id('spieler_select_breadcrumb_chzn')
            playerMenu.click()

            allPlayers = playerMenu.find_elements_by_class_name('active-result')

          playerStart = 0

          isClubCompleted = True

          clubMenu = driver.find_element_by_id('verein_select_breadcrumb_chzn')
          clubMenu.click()

          allClubs = clubMenu.find_elements_by_class_name('active-result')

        clubStart = 0

        isCompetitionCompleted = True

        competitionMenu = driver.find_element_by_id('wettbewerb_select_breadcrumb_chzn')
        competitionMenu.click()

        allCompetitions = competitionMenu.find_elements_by_class_name('active-result')

        competionStart = 0

    isCountryCompleted = True

    countryMenu = driver.find_element_by_id('land_select_breadcrumb_chzn')
    countryMenu.click()

if(__name__ == '__main__'):
    print("Transfermakt scraper is starting...")
    while True:
        try:
          parser(countryBreakPoint, competitionBreakPoint, clubBreakPoint, playerBreakPoint)
          break
        except Exception as e:
          print(str(e))
          globals().get('driver').close()

          if isCountryCompleted is True:
            countryBreakPoint += 1
          if isCompetitionCompleted is True:
            competitionBreakPoint += 1
          if isClubCompleted is True:
            clubBreakPoint += 1
          if isPlayerCompleted is True:
            playerBreakPoint += 1

          print("Resuming on: " + str(competitionBreakPoint) + ", " + str(competitionBreakPoint) + ", " + str(clubBreakPoint) + ", " + str(playerBreakPoint))
          pass