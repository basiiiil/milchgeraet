from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from lxml import html
import requests
from selenium.webdriver.firefox.options import Options
import datetime


# Parameter für Wetten:
grenzratio = 1.03
grenzavg = 15
globalazq = 0.93
globaltax = 0.95
numruns = 50000
bookieslist = ["bet365", "Betano.de", "betano.de", "Betano", "betano", "William Hill", "Unibet", "Bethard", "BetOlimp", "Betsafe"]

options = Options()
options.headless = True

def sendtosheet(payload):
    gurl = "https://script.google.com/macros/s/AKfycbxad7O3CW8bYYyvpH2kSBr8eMzDMBLFtL0B4JezJ3fglQYXR7A/exec"
    requests.get(gurl, params=payload)

def corr_time(value):
    hourold = int(value[11:13])
    if hourold < 9:
        hournew = "0" + str(hourold + 1)
        datenew = value[6:10] + "-" + value[3:5] + "-" + value[0:2] + " " + hournew + value[13:16] + ":00"
    elif hourold == 23:
        dayold = int(value[0:2])
        daynew = str(dayold + 1)
        datenew = value[6:10] + "-" + value[3:5] + "-" + daynew + " 00" + value[13:16] + ":00"
    # elif hourold == 23:
        # dayold = int(value[0:2])
        # daynew = str(dayold + 1)
        # datenew = value[6:10] + "-" + value[3:5] + "-" + daynew + " 01" + value[13:16] + ":00"
    else:
        hournew = str(hourold + 1)
        datenew = value[6:10] + "-" + value[3:5] + "-" + value[0:2] + " " + hournew + value[13:16] + ":00"
    return datenew

for ix in range(numruns):

    driver = webdriver.Firefox(options=options)
    time.sleep(1)
    url = 'https://www.betbrain.com/next-matches/'

    driver.get(url)
    time.sleep(1)

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//form[@class="Form"]//input[@id="InputEmail"]'))
        )
    except:
        driver.quit()
        rightnow = str(datetime.datetime.now())
        print(rightnow + " - could't log in")
        time.sleep(5)
        continue
    else:
        try:
            loginelem = driver.find_element_by_xpath('//form[@class="Form"]//input[@id="InputEmail"]')
            passelem = driver.find_element_by_xpath('//form[@class="Form"]//input[@id="InputPassword"]')
            lgnbtn = driver.find_element_by_xpath('//form[@class="Form"]//button[@class="PrimaryButton LoginBTN"]')
            time.sleep(0.3)
            loginelem.send_keys("boostking")
            time.sleep(0.3)
            passelem.send_keys("Sanderstrasse:1000")
            time.sleep(0.3)
            lgnbtn.send_keys(Keys.RETURN)
            rightnow = str(datetime.datetime.now())
            print(rightnow + " - Login successsful (run nr. " + str(ix) + ")")
        except:
            driver.quit()
            rightnow = str(datetime.datetime.now())
            print(rightnow + " - could't log in - Version 2")
            time.sleep(5)
            continue
        else:
            time.sleep(2)

        for x in range(35):
            try:
                mrebtnwt = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//button[@class="Button SportsBoxAll LoadMore"]'))
                )
            except:
                rightnow = str(datetime.datetime.now())
                print(rightnow + " - page " + str(x+1) + " (last page)")
                time.sleep(1)
                break
            else:
                try:
                    time.sleep(1)
                    mrebtn = driver.find_element_by_xpath('//button[@class="Button SportsBoxAll LoadMore"]')
                    time.sleep(0.5)
                    mrebtn.send_keys(Keys.RETURN)
                except:
                    rightnow = str(datetime.datetime.now())
                    print(rightnow + " - couldn't find 'LoadMore' button - Version 2")
                    continue
                else:
                    if x == 0 or (x+1)%5 == 0:
                        rightnow = str(datetime.datetime.now())
                        print(rightnow + " - page " + str(x+1))
            finally:
                time.sleep(1)


        rightnow = str(datetime.datetime.now())
        print(rightnow + " - got all pages")
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

                    # Für Bookies ohne Wettsteuer:
                    spBookies2 = ["Babibet", "Betfair", "Tipico", "Bethard", "BetOlimp"]
                    if Bookie in spBookies2:
                        Ratio = round((Quote * globalazq / AVG), 3)
                    else:
                        Ratio = round((Quote * globalazq * globaltax / AVG), 3)
                        
                    testBookies = ["BetOlimp"]
                    if Bookie in testBookies:
                        grenzratio = 1.045
                        

                    if Ratio > grenzratio and AVG <= grenzavg and Bookie in bookieslist:
                        HomeTeam = Match.xpath(".//div[@class='MatchDetails']/a/span/span[1]/text()")[0]
                        AwayTeam = Match.xpath(".//div[@class='MatchDetails']/a/span/span[3]/text()")[0]

                        DaTitemp = Match.xpath(".//span[@class='DateTime']/time/text()")[0]
                        DaTi = corr_time(DaTitemp)

                        tempLink1 = Match.xpath(".//a[@class='MatchTitleLink']/@href")[0]
                        tempLink2 = tempLink1.split("#")
                        MatchLink = "https://www.betbrain.com" + tempLink2[0]

                        f = open("duples.txt", "r")
                        dupelines = f.readlines()
                        f.close()
                        checkvar = HomeTeam + AwayTeam + HDA + Bookie + "\n"

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
                            "DateTimeVar": DaTi,
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

                            rightnow = str(datetime.datetime.now())
                            print(rightnow + " - +++++ OPPORTUNITY SENT!!! (" + Bookie + ")+++++")


                            f2 = open("duples.txt", "w")
                            for line in dupelines[1:]:
                                f2.write(line)
                            f2.write(HomeTeam + AwayTeam + HDA + Bookie + "\n")
                            f2.close()

                            time.sleep(0.5)

    finally:
        driver.quit()
        rightnow = str(datetime.datetime.now())
        print(rightnow + " - done")
        time.sleep(5)
        rightnow = str(datetime.datetime.now())
        print(rightnow + " - ...waiting: start...")
        time.sleep(85)
        rightnow = str(datetime.datetime.now())
        print(rightnow + " - ...waiting: halftime...")
        time.sleep(90)
        rightnow = str(datetime.datetime.now())
        print(rightnow + " - ...waiting: finished!...")
