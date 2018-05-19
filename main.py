from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument("--headless")

browser = webdriver.Firefox(executable_path="/home/toor/Desktop/firefoxGeckoDriver/geckodriver", firefox_options=options)

transferMarktBaseUrl = "https://www.transfermarkt.com.tr"

browser.get(transferMarktBaseUrl)

deneme = browser.find_element_by_xpath("//div[@class ='subKategorie']")

print (deneme.text)