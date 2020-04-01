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


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
#
#         GLOBAL CONSTANTS

grenzratio = 1
grenzavg = 15
globalazq = 0.95
globaltax = 0.95
numruns = 50000
activeBookies = [
    "bet365",
    "Tipico",
    "Betano.de",
    "Unibet",
    "Bethard",
    "BetOlimp",
    "Betsafe"
]
basilsBookies = [
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

#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ # 




def sendToGoogle(payload):
    gurl = "https://script.google.com/macros/s/AKfycbxad7O3CW8bYYyvpH2kSBr8eMzDMBLFtL0B4JezJ3fglQYXR7A/exec"
    requests.get(gurl, params=payload)

# Meine gurl: "https://script.google.com/macros/s/AKfycbxf4_c6BEXWc-HQkD-AB1eZRRvoY5UahGAtvIfTGfJXVIetESzZ/exec"
# BasilsBot chat_id: 701987049


def sendToBasilsBot(msg):
    telegramUrl = "https://api.telegram.org/bot1079228725:AAFBZd5qkfqkQC2Pm3UCj-wY90T0vmCUI6Y"
    newUrl = telegramUrl + "/sendMessage?chat_id=701987049&text=" + msg + "&parse_mode=HTML"
    requests.post(newUrl)
   

def sendToBoostBot(msg):
    telegramUrl = "https://api.telegram.org/bot632005608:AAGkgrZBxk1fmKb2nTpx5jEENr6UacEsbKc"
    newUrl = telegramUrl + "/sendMessage?chat_id=-1001342120887&text=" + msg + "&parse_mode=MarkdownV2"
    requests.post(newUrl)


def corr_time(value):
    tday = datetime.now()
    bbDate = datetime.strptime(value, "%d/%m/%Y %H:%M")
    newdate = bbDate + timedelta(hours=2)
    
    if newdate.day == tday.day:
        return "Heute " + newdate.strftime("%H:%M")
    elif newdate.day == tday.day+1:
        return "Morgen " + newdate.strftime("%H:%M")
    else:
        return newdate.strftime("%d/%m/%Y %H:%M")


def getNextMatchesHtml(driver):

    url = 'https://www.betbrain.com/next-matches/'
    driver.get(url)
    time.sleep(2)

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//form[@class="Form"]//input[@id="InputEmail"]'))
        )
    except Exception:
        driver.quit()
        sendToBasilsBot("LogInFindError")
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
            
        except Exception:
            driver.quit()
            sendToBasilsBot("LogInInputError")
            time.sleep(10)
            sys.exit()
        else:
            time.sleep(4)
            
            try:
                filterelem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="favorite-filters cs-select"]'))
                )
            except Exception:
                driver.quit()
                sendToBasilsBot("FilterFindError")
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
            

                for x in range(70):
                    try:
                        mrebtnwt = WebDriverWait(driver, 6).until(
                            EC.presence_of_element_located((By.XPATH, '//button[@class="Button SportsBoxAll LoadMore"]'))
                        )
                    except Exception:
                        break
                    else:
                        try:
                            time.sleep(1)
                            mrebtn = driver.find_element_by_xpath('//button[@class="Button SportsBoxAll LoadMore"]')
                            time.sleep(0.5)
                            mrebtn.send_keys(Keys.RETURN)
                        except Exception:
                            continue
                    finally:
                        time.sleep(1)

    finally:
        try:
            ulElem = driver.find_element_by_xpath('//ul[@class="MatchesList"]')
            time.sleep(2)
        except Exception:
            driver.quit()
            sendToBasilsBot("MatchesListFindError")
            time.sleep(1)
            sys.exit()
        else:
            try:
                htmldoc = ulElem.get_attribute('innerHTML')
                time.sleep(2)
            except Exception:
                driver.quit()
                sendToBasilsBot("GetAttributeError")
                time.sleep(1)
                sys.exit()
            else:
                try:
                    tree = html.fromstring(htmldoc)
                    time.sleep(2)
                except Exception:
                    driver.quit()
                    sendToBasilsBot("fromStringError")
                    time.sleep(1)
                    sys.exit()
                else:
                    rightnow = datetime.now().strftime("%x %X")
                    print(rightnow + " - First step successful")

                    return tree





def getGoodLinks(tree):

    linkList = []
    theGoodList = []

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
                
                tempLink = Match.xpath(".//a[@class='MatchTitleLink']/@href")[0]
                MatchLink = "https://www.betbrain.com" + tempLink
                
                Sport = tempLink.split("/")[1]

                HomeTeam = Match.xpath(".//div[@class='MatchDetails']/a/span/span[1]/text()")[0]
                AwayTeam = Match.xpath(".//div[@class='MatchDetails']/a/span/span[3]/text()")[0]

                DaTitemp = Match.xpath(".//span[@class='DateTime']/time/text()")[0]
                DaTi = corr_time(DaTitemp)

                # Für Bookies ohne Wettsteuer:
                spBookies2 = ["Babibet", "Betfair", "Tipico", "BetOlimp"]
                
                if Bookie in spBookies2:
                    Ratio = round((Quote * globalazq / AVG), 2)
                else:
                    Ratio = round((Quote * globalazq * globaltax / AVG), 2)

                if Ratio > grenzratio and AVG <= grenzavg and MatchLink not in linkList:
                    linkList.append(MatchLink)
                    theGoodList.append([HomeTeam, AwayTeam, DaTi, MatchLink])

                    print(Bookie, HomeTeam, HDA, Ratio, Quote, AVG)

    # print([linkList, homeTeamList, awayTeamList, dateTimeList])

    return [linkList, theGoodList]



def getSingleMatchHtml(driver, url ):

    driver.get(url)
    time.sleep(2)

    try:
        tableElem = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="OTBookmakers"]/parent::*'))
        )
    except Exception:
        sendToBasilsBot("FindBookmakersTableError")
        return None
    else:
        try:
            htmldoc = tableElem.get_attribute('innerHTML')
            time.sleep(0.5)
        except Exception:
            sendToBasilsBot("GetAttributeError2")
            return None
        else:
            try:
                tree = html.fromstring(htmldoc)
                time.sleep(0.5)
            except Exception:
                sendToBasilsBot("fromStringError2")
                return None
            else:
                return tree



def getBookiesCol(tree):

    bookiesList = []
    azqList = []

    for bookieLine in tree.xpath('.//li[contains(@class,"OTBookieContainer")]'):

        try: 

            bookie = bookieLine.xpath('.//span[@class="BookieLogo BL"]/span/text()')[0]
            if bookie == "Betfair":
                continue

            azqString = bookieLine.xpath('.//span[@class="Payout"]/text()')[0]
            azq = int(azqString[:-1]) / 100

        except Exception:
            print("fail")
            continue

        else:
            bookiesList.append(bookie)
            azqList.append(azq)

    return [bookiesList, azqList]



def getOddsListPerBookie(oddsRow):

    oddsListPerBookieTemp =[]
    oddsListPerBookie = [1,1,1]

    for oddsField in oddsRow:
        try:
            odd = float(oddsField.xpath('./a/span/span/text()')[0])

        except Exception:
            oddsListPerBookieTemp.append("weird")

        else:
            oddsListPerBookieTemp.append(odd)

    if len(oddsListPerBookieTemp) == 2:
        oddsListPerBookie[0] = oddsListPerBookieTemp[0]
        oddsListPerBookie[2] = oddsListPerBookieTemp[1]
    else:
        oddsListPerBookie[0] = oddsListPerBookieTemp[0]
        oddsListPerBookie[1] = oddsListPerBookieTemp[1]
        oddsListPerBookie[2] = oddsListPerBookieTemp[2]

    return oddsListPerBookie



def getAvg(tree):

    avgListTemp = []
    avgList = [5,5,5]

    for avgField in tree.xpath('.//div[@class="OTBookmakersStatsOdds"]/ul[1]/li[@class="OTCol IsAverage"]'):
        try:
            avg = float(avgField.xpath('./text()')[0])

        except Exception:
            avgListTemp.append("weird 2")

        else:
            avgListTemp.append(avg)

    if len(avgListTemp) == 2:
        avgList[0] = avgListTemp[0]
        avgList[2] = avgListTemp[1]
    else:
        avgList[0] = avgListTemp[0]
        avgList[1] = avgListTemp[1]
        avgList[2] = avgListTemp[2]

    return avgList



def getRatio(quoten, azq, avgs):
    ratios = []

    for k in range(3):
        ratioTemp = round((quoten[k] * azq * 0.95 / avgs[k]), 2)
        ratios.append(ratioTemp)

    return ratios

                                
                                
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            #
            #         send message 1 if good
            #
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def getDemNumbers(tree, avgs):

    oddsListTotal = []
    listComplete = []

    bookiesCol = getBookiesCol(tree)
    bookiesList = bookiesCol[0]
    azqList = bookiesCol[1]

    oddsRows = tree.xpath('.//ul[@class="OTRow"]')

    for i in range(len(bookiesList)):
        oddsListPerBookie = getOddsListPerBookie(oddsRows[i])
        oddsListTotal.append(oddsListPerBookie)

    for row in range(len(bookiesList)):
        quoten = oddsListTotal[row]
        azq = azqList[row]
        
        ratios = getRatio(quoten, azq, avgs)

        listComplete.append([bookiesList[row], quoten, ratios])

        # print([bookiesList[row], azq, quoten, ratios])

    return listComplete




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
    
    # sendtosheet2("finished!")
    # rightnow = datetime.now().strftime("%x %X")
    # print(rightnow + " - finished!")






driver = webdriver.Firefox(options=options)
time.sleep(5)




nmTree = getNextMatchesHtml(driver)

goodLinks = getGoodLinks(nmTree)
linkList = goodLinks[0]
goodLinksList = goodLinks[1]


matchTreeList = []

for link in linkList:
    rightnow = datetime.now().strftime("%x %X")
    print(rightnow + " - getting MatchTree " + str(linkList.index(link) + 1) + " of " + str(len(linkList)))
    
    smTree = getSingleMatchHtml(driver, link)
    matchTreeList.append(smTree)

#quoten = oddsListTotal[row]
# azq = azqList[row]

# ratios = getRatio(oddsCount, quoten, azq, avgs)
#[bookiesList[row], quoten, ratios]

driver.quit()

theFinalList = []

for b in range(len(goodLinksList)):
    spiel = goodLinksList[b]
    averages = getAvg(matchTreeList[b])
    numbersPerMatch = getDemNumbers(matchTreeList[b], averages)
    # print(numbersPerMatch)

    theFinalList.append({
        "HomeTeam": spiel[0],
        "AwayTeam": spiel[1],
        "DaTi": spiel[2],
        "MatchLink": spiel[3],
        "Sport": spiel[3].split('#')[0].split("/")[3],
        "Country": spiel[3].split('#')[0].split("/")[4],
        "Tour": spiel[3].split('#')[0].split("/")[5],
        "AVG": averages,
        "Odds": numbersPerMatch
        })


# print(theFinalList)


for match in theFinalList:

    for row in match["Odds"]:

        for n in range(3):
            Bookie = row[0]
            Ratio = row[2][n]

            if Ratio > grenzratio and Bookie in activeBookies:

                # f = open("/home/basil/Dokumente/MilkMachine/duples.txt", "r")
                # dupelines = f.readlines()
                # f.close()

                f = open("duples.txt", "r")
                dupelines = f.readlines()
                f.close()

                HomeTeam = match["HomeTeam"]
                AwayTeam = match["AwayTeam"]
                if n == 0:
                    HDA = "Home"
                elif n == 1:
                    HDA = "Draw"
                else:
                    HDA = "Away"
                DaTi = match["DaTi"]
                MatchLink = match["MatchLink"]
                Quote = row[1][n]
                AVG = match["AVG"][n]

                checkvar = HomeTeam + AwayTeam + HDA + Bookie + "\n"

                # dupelines = ["kjhfb", "shdb"]

                if checkvar not in dupelines:
                    rightnow = datetime.now().strftime("%x %X")
                    print(rightnow + HomeTeam + " not in dupelines")

                    Sport = match["Sport"]
                    Country = match["Country"]
                    Tour = match["Tour"]
                    
                    
                    forsheet4 = ("<i>Bookie:</i> <b>" + Bookie +
                        "<b/>%0A%0A<b>" + HomeTeam + " vs. " + AwayTeam +
                        "<b/>%0A%0A<i>Time:</i>  " + DaTi +
                        "%0A<i>Sport:</i>  " + Sport +
                        "%0A<i>in:</i>  " + Country + ": " + Tour +
                        "%0A%0A<i>Wette:</i>     <a href=" + MatchLink + ">" + HDA + "</a>" 
                        ")%0A<i>Ratio:</i>      <b>" + str(Ratio) +
                        "<b/>%0A<i>Quote:</i>     <b>" + str(Quote) +
                        "<b/>%0A<i>avg:</i>         " + str(AVG))

                    forsheet3 = ("<i>Bookie:</i> <b>" + Bookie +
                        "<b/>%0A%0A<b>" + HomeTeam + " vs. " + AwayTeam +
                        "<b/>%0A%0A<i>Time:</i>  " + DaTi +
                        "%0A<i>Sport:</i>  " + Sport +
                        "%0A<i>in:</i>  " + Country + ": " + Tour +
                        "%0A%0A<i>Wette:</i>     [" + HDA + "](" + MatchLink +
                        ")%0A<i>Ratio:</i>      <b>" + str(Ratio) +
                        "<b/>%0A<i>Quote:</i>     <b>" + str(Quote) +
                        "<b/>%0A<i>avg:</i>         " + str(AVG))

                    # sendToBoostBot(forsheet3)
                    try:
                        sendToBasilsBot(forsheet4)
                    except Exception:
                        rightnow = datetime.now().strftime("%x %X")
                        print(rightnow + " FAIL 1")
                    else:
                        rightnow = datetime.now().strftime("%x %X")
                        print(rightnow + " Yeah!")        
                    
                    # f2 = open("/home/basil/Dokumente/MilkMachine/duples.txt", "w")
                    # for line in dupelines[1:]:
                    #     f2.write(line)
                    # f2.write(checkvar)
                    # f2.close()

                    f2 = open("duples.txt", "w")
                    for line in dupelines[1:]:
                        f2.write(line)
                    f2.write(checkvar)
                    f2.close()


                    time.sleep(0.5)