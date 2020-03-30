from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from lxml import html
import requests
from selenium.webdriver.firefox.options import Options
from datetime import datetime, timedelta
import sys


# Parameter für Wetten:
grenzratio = 1.02
grenzavg = 15
globalazq = 0.93
globalazq2 = 0.88
globaltax = 0.95
numruns = 50000
bookieslist = [
    "bet365",
    "Tipico",
    #"Betano.de",
    # "Unibet",
    # "Bethard",
    # "BetOlimp",
    # "Betsafe"
]
bookieslist2 = [
    # "Betano.de",
    "Unibet",
    "Bethard",
    # "BetOlimp",
    # "Betsafe",
    # "William Hill"
]
testBookies = ["BetOlimp"]

today = datetime.now()
todayDate = today.strftime("%d/%m/%Y")
yesterday = today - timedelta(days=1)
ystrdyDate = yesterday.strftime("%d/%m/%Y")
beforeyes = today - timedelta(days=2)
befyesDate = beforeyes.strftime("%d/%m/%Y")
rightnow = today.strftime("%H%M")
chckpnts = ["0500", "1000", "1620", "2000"]

options = Options()
options.headless = True
# rightnow = datetime.datetime.now().strftime("%x %X")
# print(rightnow + " - started script")

def sendToGoogle(payload):
    gurl = "https://script.google.com/macros/s/AKfycbxad7O3CW8bYYyvpH2kSBr8eMzDMBLFtL0B4JezJ3fglQYXR7A/exec"
    requests.get(gurl, params=payload)

# Meine gurl: "https://script.google.com/macros/s/AKfycbxf4_c6BEXWc-HQkD-AB1eZRRvoY5UahGAtvIfTGfJXVIetESzZ/exec"
# BasilsBot chat_id: 701987049

def sendToBasilsBot(msg):
    telegramUrl = "https://api.telegram.org/bot1079228725:AAFBZd5qkfqkQC2Pm3UCj-wY90T0vmCUI6Y"
    newUrl = telegramUrl + "/sendMessage?chat_id=701987049&text=" + msg + "&parse_mode=MARKDOWN"
    requests.post(newUrl)
    
# send to BoostBot:
def sendToBoostBot(msg):
    telegramUrl = "https://api.telegram.org/bot632005608:AAGkgrZBxk1fmKb2nTpx5jEENr6UacEsbKc"
    newUrl = telegramUrl + "/sendMessage?chat_id=-1001342120887&text=" + msg + "&parse_mode=MARKDOWN"
    requests.post(newUrl)

def corr_time(value):
    tday = datetime.now()
    bbDate = datetime.strptime(value, "%d/%m/%Y %H:%M")
    newdate = bbDate + timedelta(hours=1)
    
    if newdate.day == tday.day:
        return "Heute " + newdate.strftime("%H:%M")
    elif newdate.day == tday.day+1:
        return "Morgen " + newdate.strftime("%H:%M")
    else:
        return newdate.strftime("%d/%m/%Y %H:%M")
    
    #hourold = int(value[11:13])
    #if hourold < 9:
        #hournew = "0" + str(hourold + 1)
        #datenew = value[6:10] + "-" + value[3:5] + "-" + value[0:2] + " " + hournew + value[13:16] + ":00"
        
    #elif hourold == 23:
        #dayold = int(value[0:2])
        #daynew = str(dayold + 1)
        #datenew = value[6:10] + "-" + value[3:5] + "-" + daynew + " 00" + value[13:16] + ":00"
    ## elif hourold == 23:
        ## dayold = int(value[0:2])
        ## daynew = str(dayold + 1)
        ## datenew = value[6:10] + "-" + value[3:5] + "-" + daynew + " 01" + value[13:16] + ":00"
    #else:
        #hournew = str(hourold + 1)
        #datenew = value[6:10] + "-" + value[3:5] + "-" + value[0:2] + " " + hournew + value[13:16] + ":00"
    #return datenew

# sendtosheet2("script started")
driver = webdriver.Firefox(options=options)
time.sleep(1)
url = 'https://www.betbrain.com/next-matches/'

driver.get(url)
time.sleep(5)

# rightnow = datetime.now().strftime("%x %X")
# print(rightnow + " - started browser")


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
#
#         find and close Ad-PopUp
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ # 

#try:
    #element = WebDriverWait(driver, 15).until(
        #EC.presence_of_element_located((By.XPATH, '//button[contains(@class,"richmond-CloseButton")]'))
    #)
#except:
    #rightnow = str(datetime.now())
    #sendToBasilsBot(rightnow + " - could't find Richmond")
    #driver.quit()
    #time.sleep(5)
    #continue
#else:
    #rightnow = str(datetime.now())
    #sendToBasilsBot(rightnow + " - found Richmond")
    #time.sleep(2)
    #try:
        #richbtn = driver.find_element_by_xpath('//button[contains(@class,"richmond-CloseButton")]')
        #richbtn.send_keys(Keys.RETURN)
        #time.sleep(1)
    #except:
        #rightnow = str(datetime.now())
        #sendToBasilsBot(rightnow + " - could't reach Richmond")
        #driver.quit()
        #time.sleep(5)
        #continue
    
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
#
#         Login
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ # 
try:
    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//form[@class="Form"]//input[@id="InputEmail"]'))
    )
except:
    driver.quit()
    sendToBasilsBot("LogInFindError")
    # rightnow = datetime.now().strftime("%x %X")
    # print(rightnow + " - LogInFindError")
    time.sleep(5)
    sys.exit()
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
        
    except:
        driver.quit()
        sendToBasilsBot("LogInInputError")
        # rightnow = datetime.now().strftime("%x %X")
        # print(rightnow + " - LogInInputError")
        time.sleep(10)
        sys.exit()
    else:
        # sendToBasilsBot("Login successful")
        # rightnow = datetime.now().strftime("%x %X")
        # print(rightnow + " - Login successful")
        time.sleep(5)
        
        try:
            filterelem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="favorite-filters cs-select"]'))
            )
        except:
            driver.quit()
            sendToBasilsBot("FilterFindError")
            # rightnow = datetime.now().strftime("%x %X")
            # print(rightnow + " - FilterFindError")
            time.sleep(5)
            sys.exit()
        else:
            filterelem.click()
            time.sleep(0.3)
            myfilterelem = driver.find_element_by_xpath('//div[@class="favorite-filters cs-select active"]//li/span')
            myfilterelem.click()
            time.sleep(0.3)
            filterbtn = driver.find_element_by_xpath('//button[@class="PrimaryButton FilterSubmit"]')
            filterbtn.click()
            time.sleep(0.3)
        






# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
#
#         getting all pages (max. 70)
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ # 

    for x in range(70):
        try:
            mrebtnwt = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[@class="Button SportsBoxAll LoadMore"]'))
            )
        except:
            # sendToBasilsBot("page " + str(x+1) + " (last page)")
            # rightnow = datetime.now().strftime("%x %X")
            # print(rightnow + " - page " + str(x+1) + " (last page)")
            time.sleep(1)
            break
        else:
            try:
                time.sleep(1)
                mrebtn = driver.find_element_by_xpath('//button[@class="Button SportsBoxAll LoadMore"]')
                time.sleep(0.5)
                mrebtn.send_keys(Keys.RETURN)
            except:
                # sendToBasilsBot("couldn't find 'LoadMore' button - Version 2")
                # print("couldn't find 'LoadMore' button - Version 2")
                continue
            # else:
                # if x == 0 or (x+1)%10 == 0:
                    # sendToBasilsBot("page " + str(x+1))
                    # rightnow = datetime.now().strftime("%x %X")
                    # print(rightnow + " - page " + str(x+1))
        finally:
            time.sleep(1)


    time.sleep(3)
    # sendToBasilsBot("got all pages")
    # rightnow = datetime.now().strftime("%x %X")
    # print(rightnow + " - got all pages")
    try:
        ulElem = driver.find_element_by_xpath('//ul[@class="MatchesList"]')
        time.sleep(2)
    except Exception:
        driver.quit()
        time.sleep(1)
        sendToBasilsBot("MatchesListFindError")
        sys.exit()
    else:
        try:
            htmldoc = ulElem.get_attribute('innerHTML')
            # htmldoc = driver.page_source
            time.sleep(2)
        except Exception:
            driver.quit()
            time.sleep(1)
            sendToBasilsBot("GetAttributeError")
            # rightnow = datetime.now().strftime("%x %X")
            # print(rightnow + " - pageSourceError")
            sys.exit()
        else:
            try:
                tree = html.fromstring(htmldoc)
                time.sleep(2)
            except Exception:
                driver.quit()
                time.sleep(1)
                sendToBasilsBot("fromStringError")
                # rightnow = datetime.now().strftime("%x %X")
                # print(rightnow + " - fromStringError")
                sys.exit()
            else:
                if rightnow in chckpnts:
                    sendToBasilsBot("- still running -")

        
        
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    #
    #         loop through matches and calculate quotes
    #
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ # 


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
                            
                            tempLink1 = Match.xpath(".//a[@class='MatchTitleLink']/@href")[0]
                            tempLink2 = tempLink1.split("#")
                            MatchLink = "https://www.betbrain.com" + tempLink2[0]
                            
                            tempSport = tempLink1.split("/")
                            Sport = tempSport[1]

                            # Für Bookies ohne Wettsteuer:
                            spBookies2 = ["Babibet", "Betfair", "Tipico", "BetOlimp"]
                            
                            if Sport == "football":
                                if Bookie in spBookies2:
                                    Ratio = round((Quote * globalazq / AVG), 2)
                                else:
                                    Ratio = round((Quote * globalazq * globaltax / AVG), 2)
                            else:
                                if Bookie in spBookies2:
                                    Ratio = round((Quote * globalazq2 / AVG), 2)
                                else:
                                    Ratio = round((Quote * globalazq2 * globaltax / AVG), 2)
                                
                                
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            #
            #         send message 1 if good
            #
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ # 
                                

                            if Ratio > grenzratio and AVG <= grenzavg and Bookie in bookieslist:
                                HomeTeam = Match.xpath(".//div[@class='MatchDetails']/a/span/span[1]/text()")[0]
                                AwayTeam = Match.xpath(".//div[@class='MatchDetails']/a/span/span[3]/text()")[0]
                                
                                #sendToBasilsBot("good Opp (" + Bookie + ") " + HomeTeam)

                                DaTitemp = Match.xpath(".//span[@class='DateTime']/time/text()")[0]
                                DaTi = corr_time(DaTitemp)


                                f = open("/home/basil/Dokumente/MilkMachine/duples.txt", "r")
                                dupelines = f.readlines()
                                f.close()
                                checkvar = HomeTeam + AwayTeam + HDA + Bookie + "\n"

                                if checkvar not in dupelines:

                                    tempCountry = tempLink1.split("/")
                                    Country = tempCountry[2]

                                    tempTour = tempLink1.split("/")
                                    Tour = tempTour[3]


                                    #forsheet = {
                                    #"BookieVar": Bookie,
                                    #"HomeTeamVar": HomeTeam,
                                    #"AwayTeamVar": AwayTeam,
                                    #"DateTimeVar": DaTi,
                                    #"SportVar": Sport,
                                    #"CountryVar": Country,
                                    #"TourVar": Tour,
                                    #"HDAVar": HDA,
                                    #"MatchLinkVar": MatchLink,
                                    #"RatioVar": Ratio,
                                    #"QVar": Quote,
                                    #"AVGVar": AVG
                                    #}
                                    
                                    #sendtosheet(forsheet)
                                    # sendToBasilsBot("OPPORTUNITY SENT! (" + Bookie + ")")
                                    
                                    # rightnow = datetime.now().strftime("%x %X")
                                    # print(rightnow + " - OPPORTUNITY SENT!!! (" + Bookie + ")")
                                    
                                    forsheet3 = "_Bookie:_ *" + Bookie + "*%0A%0A*" + HomeTeam + " vs. " + AwayTeam + "*%0A%0A_Time:_  " + DaTi + "%0A_Sport:_  " + Sport + "%0A_in:_  " + Country + ": " + Tour + "%0A%0A_Wette:_     [" + HDA + "](" + MatchLink + ")%0A_Ratio:_      *" + str(Ratio) + "*%0A_Quote:_     *" + str(Quote) + "*%0A_avg:_         " + str(AVG)

                                    sendToBoostBot(forsheet3)                                
                                    
                                    f2 = open("/home/basil/Dokumente/MilkMachine/duples.txt", "w")
                                    for line in dupelines[1:]:
                                        f2.write(line)
                                    f2.write(HomeTeam + AwayTeam + HDA + Bookie + "\n")
                                    f2.close()


                                    time.sleep(0.5)
                                    
                                    liveScoresFile = open("/home/basil/Dokumente/MilkMachine/CurrentMatches.txt", "r")
                                    liveScoresOld = liveScoresFile.readlines()
                                    liveScoresFile.close()
                                    
                                    liveScoresFile2 = open("/home/basil/Dokumente/MilkMachine/CurrentMatches.txt", "w")
                                    for line in liveScoresOld:
                                        liveScoresFile2.write(line)
                                    liveScoresFile2.write(HomeTeam + " vs. " + AwayTeam + "," + DaTitemp + "," + MatchLink + ",\n")
                                    liveScoresFile2.close()
                                    
                                    
                                    
                                    
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            #
            #         send message 2 if good
            #
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ # 
                            
                            elif Ratio >= 1.01 and AVG <= grenzavg and Bookie in bookieslist2:
                                HomeTeam = Match.xpath(".//div[@class='MatchDetails']/a/span/span[1]/text()")[0]
                                AwayTeam = Match.xpath(".//div[@class='MatchDetails']/a/span/span[3]/text()")[0]
                                
                                # sendToBasilsBot("good Opp 2 (" + Bookie + ") " + HomeTeam)

                                DaTitemp = Match.xpath(".//span[@class='DateTime']/time/text()")[0]
                                
                                DaTi = corr_time(DaTitemp)
                                
                                tempLink1 = Match.xpath(".//a[@class='MatchTitleLink']/@href")[0]
                                tempLink2 = tempLink1.split("#")
                                MatchLink = "https://www.betbrain.com" + tempLink2[0]
                                
                                f = open("/home/basil/Dokumente/MilkMachine/duples.txt", "r")
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
                                                                    
                                    forsheet2 = "_Bookie:_ *" + Bookie + "*%0A%0A*" + HomeTeam + " vs. " + AwayTeam + "*%0A%0A_Time:_  " + DaTi + "%0A_Sport:_  " + Sport + "%0A_in:_  " + Country + ": " + Tour + "%0A%0A_Wette:_     [" + HDA + "](" + MatchLink + ")%0A_Ratio:_      *" + str(Ratio) + "*%0A_Quote:_     *" + str(Quote) + "*%0A_avg:_         " + str(AVG)
                                    
                                    sendToBasilsBot(forsheet2)

                                    # rightnow = datetime.now().strftime("%x %X")
                                    # print(rightnow + " - OPPORTUNITY SENT! (" + Bookie + ") - (2)")
                                    
                                    f2 = open("/home/basil/Dokumente/MilkMachine/duples.txt", "w")
                                    for line in dupelines[1:]:
                                        f2.write(line)
                                    f2.write(HomeTeam + AwayTeam + HDA + Bookie + "\n")
                                    f2.close()


                                    time.sleep(0.5)
                        
                        
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
#
#         close and wait for next round
#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ # 

finally:
    #f8 = open("/home/basil/Dokumente/MilkMachine/CurrentMatches.txt", "r")
    #currMatches = f8.readlines()
    #f8.close()

    #runIt = False

    #for i in range(len(currMatches)):
        #currTeam = currMatches[i].split(",")[0]
        #currDate = currMatches[i].split(",")[1].split(" ")[0]
        #currDate2 = currMatches[i].split(",")[1].split(" ")[0]
        #print(currTeam + "  " + currDate + "  " + currDate2)
        #currHour = currMatches[i].split(",")[1].split(" ")[1].split(":")[0]
        
        #currMin = currMatches[i].split(",")[1].split(" ")[1].split(":")[1]
        #currTimeHndr = int(currHour + currMin) + 100
        #if currTimeHndr >= 2400:
            #currTimeHndr -= 2400
        #rnTimeHndr = int(rightnow)
        
        #if currDate == todayDate and rnTimeHndr >= currTimeHndr and rnTimeHndr <= currTimeHndr+300:
            #runIt = True

    #print(str(runIt))

    #if runIt == True:
        #print("STEP 1")


        #for i in range(len(currMatches)):
            
            #currTeam = currMatches[i].split(",")[0]
            #currDate = currMatches[i].split(",")[1].split(" ")[0]
            #currHour = currMatches[i].split(",")[1].split(" ")[1].split(":")[0]
            #currMin = currMatches[i].split(",")[1].split(" ")[1].split(":")[1]
            #currTimeHndr = int(currHour + currMin) + 100
            #if currTimeHndr >= 2400:
                #currTimeHndr -= 2400
            #print(currTeam + str(currTimeHndr))
            
            #if currDate == todayDate and rnTimeHndr >= currTimeHndr and rnTimeHndr <= currTimeHndr+300:
                
                #url = currMatches[i].split(",")[2]

                #driver.get(url)
                #time.sleep(6)
                
                #try:
                    #ScoresWrapperElem = WebDriverWait(driver, 15).until(
                        #EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"ScoresContentWrapper")]'))
                    #)
                #except Exception:
                    #print("ERROR 1")
                    #driver.quit()
                    #time.sleep(1)
                    #sys.exit()
                #else:
                    #try:
                        #ScoresWrapper = driver.find_element_by_xpath('//div[contains(@class,"ScoresContentWrapper")]')
                        #htmldoc = ScoresWrapper.get_attribute('innerHTML')
                        #time.sleep(1)
                    #except Exception:
                        #print("ERROR 2")
                        #driver.quit()
                        #time.sleep(1)
                        #sys.exit()
                    #else:
                        #try:
                            #tree = html.fromstring(htmldoc)
                            #time.sleep(2)
                        #except Exception:
                            #print("ERROR 3")
                            #driver.quit()
                            #time.sleep(1)
                            #sys.exit()
                        #else:
                            #time.sleep(1)
                            
                            #try:
                                #score1 = tree.xpath('.//span[@class="ScoresData"]/span[contains(@class,"ScoresHomeData")]/text()')[0]
                                #score2 = tree.xpath('.//span[@class="ScoresData"]/span[contains(@class,"ScoresAwayData")]/text()')[0]
                                #scores = score1 + ":" + score2
                            #except Exception:
                                #print("No Score")
                                #try:
                                    #noScore = tree.xpath('./span[@class="NoScoreLabel"]/text()')[0]
                                    #if noScore == " NO LIVESCORE AVAILABLE":
                                        #scores = "n/a"
                                    #print(scores + " " + noScore)
                                #except Exception:
                                    #continue
                                    
                            #try:
                                #matchTimeTemp = tree.xpath('.//span[@class="ScoresDateWrapper"]/span[@class="ScoresDate"]/text()')[0]
                                #print(match)
                            #except Exception:
                                #print("ERROR 4")
                                
                                #synthMatchTimeMin = int(str(rnTimeHndr - currTimeHndr)[-2:])
                                #print(synthMatchTimeMin)
                                #synthMatchTimeHour = int(str(rnTimeHndr - currTimeHndr)[:-2]) * 60
                                #print(synthMatchTimeHour)
                                #synthMatchTime = str(synthMatchTimeHour + synthMatchTimeMin) + "'"
                                #print(synthMatchTime)
                                
                                
                                
                            #else:
                                #if matchTimeTemp == "FINAL SCORE":
                                    #matchTime = "FT"
                                ##else:
                                ##    matchTime = matchTimeTemp.split(" | ")[1]
                                    

                                #time.sleep(1)
                    
                                #msg = currTeam + "," + scores + "," + matchTime
                                #print(msg)
                    
                                #msgToSheet = {
                                    #"TeamsVar": currTeam,
                                    #"ScoresVar": scores,
                                    #"TimesVar": matchTime
                                #}
                                
                                #sendToGoogle(msgToSheet)
                                #if matchTime == "FT":
                                    #currMatches.pop(i)
                                    #sendToBasilsBot(msg)
                                #print(currTeam + " (" + scores + ") (" + matchTime + ")")
                                
        #liveScoresFile2 = open("/home/basil/Dokumente/MilkMachine/CurrentMatches.txt", "w")
        #for line in currMatches:
            #liveScoresFile2.write(line)
        #liveScoresFile2.close()
    
    driver.quit()
    # sendtosheet2("finished!")
    # rightnow = datetime.now().strftime("%x %X")
    # print(rightnow + " - finished!")
