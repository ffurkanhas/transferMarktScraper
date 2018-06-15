from selenium import webdriver
import time

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
  #options.add_argument('-headless')
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
          i = 0
          for player in range(playerStart, len(allPlayers)):

            isPlayerCompleted = False

            global playerBreakPoint
            playerBreakPoint = player
            player = allPlayers[player]
            playerName = player.text
            # Info about the player. First iteration throws error, after that runs clearly.
            if(i != 0):
              player_stats_all = driver.find_elements_by_class_name('auflistung')

              player_stats_main = player_stats_all[2]
              player_first_infos = driver.find_element_by_class_name('dataName')
              player_number = player_first_infos.find_element_by_tag_name('span').text
              player_name = player_first_infos.find_element_by_tag_name('h1').text
              print("Number: ", player_number)
              print("Name: ", player_name)
              for stat in player_stats_main.find_elements_by_tag_name('tr'):
                clean_info = stat.find_element_by_tag_name('td')
                print(clean_info.text)
            # Need to put every player info between this comment lines. (in if statement)
            print("\t\t\t" + playerName)

            player.click()

            playerSubmitButton = driver.find_elements_by_class_name('breadcrumb-button')
            playerSubmitButton[3].click()


            isPlayerCompleted = True

            playerMenu = driver.find_element_by_id('spieler_select_breadcrumb_chzn')
            playerMenu.click()

            allPlayers = playerMenu.find_elements_by_class_name('active-result')
            i+=1

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