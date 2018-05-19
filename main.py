import urllib.request
import bs4 as bs

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import sys

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)


def main():
  sys.stdout = Unbuffered(sys.stdout)

  options = webdriver.FirefoxOptions()
  options.add_argument('-headless')
  driver = webdriver.Firefox()#firefox_options=options)
  #driver = webdriver.Chrome('D:\chromedriver_win32\chromedriver.exe')

  driver.get('https://www.transfermarkt.com/#')
  #musabaka_sec = driver.find_element_by_xpath("//div[@id ='wettbewerb_select_breadcrumb_chzn']")

  #lig_sec = driver.find_element_by_xpath("//ul[@class='chzn-results']")
  #for lig in lig_sec.find_elements_by_tag_name('li'):

  country_click = driver.find_element_by_id('land_select_breadcrumb_chzn').click()
  chzn_select = driver.find_elements_by_class_name('chzn-results')
  i=0
  j=0
  for country in chzn_select[0].find_elements_by_tag_name('li'):
      if(i != 0):
        country_click = driver.find_element_by_id('land_select_breadcrumb_chzn').click()
        chzn_select = driver.find_elements_by_class_name('chzn-results')

      country.click()

      time.sleep(1)

      for league in chzn_select[1].find_elements_by_tag_name('li'):
        league_click = driver.find_element_by_id('wettbewerb_select_breadcrumb_chzn').click()
        chzn_select = driver.find_elements_by_class_name('chzn-results')
        league.click()
        for club in chzn_select[2].find_elements_by_tag_name('li'):
          club_click = driver.find_element_by_id('verein_select_breadcrumb_chzn').click()
          chzn_select = driver.find_elements_by_class_name('chzn-results')
          club.click()

      i+=1
'''
      for league in chzn_select[1].find_elements_by_tag_name('li'):
          if(league.text == 'Competition'): continue
          league.click()
          print('League:', league.text)
          #for club in chzn_select[2].find_elements_by_tag_name('li'):
          #    club.click()
          #    print('Club:', club.text)
'''
'''
  for i in range(0,4):
    print(len(chzn_select[i].find_elements_by_tag_name('li')))
    for some_thing in chzn_select[i].find_elements_by_tag_name('li'):
        print(some_thing.text)
  #wettbewerb_select_breadcrumb_chzn
  print(driver.current_url)
'''










if(__name__ == '__main__'):
    main()








