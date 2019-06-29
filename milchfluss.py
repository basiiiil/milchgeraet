from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from lxml import html
import requests
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True

def sendtosheet(payload):
    gurl = "https://script.google.com/macros/s/AKfycbxad7O3CW8bYYyvpH2kSBr8eMzDMBLFtL0B4JezJ3fglQYXR7A/exec"
    requests.get(gurl, params=payload)

driver = webdriver.Firefox(options=options)
driver.implicitly_wait(5)
url = 'https://www.betbrain.com/next-matches/'

driver.get(url)

try:
    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//form[@class="Form"]//input[@id="InputEmail"]'))
    )
except:
    driver.quit()
else:
    loginelem = driver.find_element_by_xpath('//form[@class="Form"]//input[@id="InputEmail"]')
    passelem = driver.find_element_by_xpath('//form[@class="Form"]//input[@id="InputPassword"]')
    lgnbtn = driver.find_element_by_xpath('//form[@class="Form"]//button[@class="PrimaryButton LoginBTN"]')
    time.sleep(0.3)
    loginelem.send_keys("boostking")
    time.sleep(0.3)
    passelem.send_keys("Sanderstrasse:1000")
    time.sleep(0.3)
    lgnbtn.send_keys(Keys.RETURN)


    # try:
    #     fltrwt = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, "//div[@class='favorite-filters cs-select']"))
    #     )
    # except:
    #     driver.quit()
    # else:
        # //div[@class='favorite-filters cs-select']//li/span
        # //div[@class='favorite-filters cs-select active']//li/span
        # //button[@class='PrimaryButton FilterSubmit']

    

    for x in range(50):
        try:
            mrebtnwt = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[@class="Button SportsBoxAll LoadMore"]'))
            )
        except:
            break
        else:
            time.sleep(0.5)
            mrebtn = driver.find_element_by_xpath('//button[@class="Button SportsBoxAll LoadMore"]')
            time.sleep(0.5)
            mrebtn.send_keys(Keys.RETURN)
            time.sleep(0.5)
            print("page" + str(x))


    htmldoc = driver.page_source
    tree = html.fromstring(htmldoc)


    for Match in tree.xpath("//li[@class='Match']"):

        for Quoten in Match.xpath(".//li[@class='Bet']"):

            try:
                Quote = float(Quoten.xpath(".//span[@class='Odds']/span[3]/text()")[0])
            except:
                continue
            else:
                AVG = float(Quoten.xpath(".//span[@class='AverageOdds']/span[2]/text()")[0])
                HDA = Quoten.xpath(".//span[@class='Odds']/span[1]/text()")[0]
                Bookie = Quoten.xpath(".//span[@class='BookieLogo BL']/text()")[0]

                Ratio = round((Quote * 0.87 / AVG), 2)

                if Ratio >= 1.05 and AVG <= 7:
                    HomeTeam = Match.xpath(".//div[@class='MatchDetails']/a/span/span[1]/text()")[0]
                    AwayTeam = Match.xpath(".//div[@class='MatchDetails']/a/span/span[3]/text()")[0]
                    DateTime = Match.xpath(".//span[@class='DateTime']/time/text()")[0]
                    tempLink1 = Match.xpath(".//a[@class='MatchTitleLink']/@href")[0]
                    tempLink2 = tempLink1.split("#")
                    MatchLink = "https://portal.betbrain.com" + tempLink2[0]

                    f = open("duples.txt", "r")
                    dupelines = f.readlines()
                    f.close()
                    checkvar = HomeTeam + AwayTeam + str(Quote) + "\n"

                    if checkvar not in dupelines:

                        tempCountry = tempLink1.split("/")
                        Country = tempCountry[2]

                        tempTour = tempLink1.split("/")
                        Tour = tempTour[3]

                        tempSport = tempLink1.split("/")
                        Sport = tempSport[1]

                        forsheet = {
                            "BookieVar": Bookie,
                            "HomeTeamVar": HomeTeam,
                            "AwayTeamVar": AwayTeam,
                            "DateTimeVar": DateTime,
                            "SportVar": Sport,
                            "CountryVar": Country,
                            "TourVar": Tour,
                            "HDAVar": HDA,
                            "MatchLinkVar": MatchLink,
                            "RatioVar": Ratio,
                            "QVar": Quote,
                            "AVGVar": AVG
                        }

                        sendtosheet(forsheet)

                    
                        f2 = open("duples.txt", "w")
                        for line in dupelines[1:]:
                            f2.write(line)
                        f2.write(HomeTeam + AwayTeam + str(Quote) + "\n")
                        f2.close()

                        time.sleep(0.5)

finally:
    driver.quit()
    print("done")
