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

grenzratio = 1.04
grenzratio2 = 1.02
grenzavg = 15
globalazq = 0.95
globaltax = 0.95
activeBookies = [
    #"bet365",
    "Tipico",
    #"Betano.de",
    #"Unibet",
    #"Bethard",
    #"BetOlimp",
    #"Betsafe"
]
basilsBookies = [
    #"bet365",
    "Betano.de",
    "Unibet",
    #"Bethard",
    #"BetOlimp",
    #"Betsafe",
    #"William Hill"
]
BookiesOhneSteuer = [
    "Babibet",
    "Betfair",
    "Tipico"
]

today = datetime.now()
todayDate = today.strftime("%d/%m/%Y")
yesterday = today - timedelta(days=1)
ystrdyDate = yesterday.strftime("%d/%m/%Y")
beforeyes = today - timedelta(days=2)
befyesDate = beforeyes.strftime("%d/%m/%Y")
rightnowStart = today.strftime("%H%M")
chckpnts = ["0500", "1000", "1412", "1500", "2000"]

options = Options()
options.headless = True

#
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ # 




def sendToGoogle(payload):
    gurl = "https://script.google.com/macros/s/AKfycbxad7O3CW8bYYyvpH2kSBr8eMzDMBLFtL0B4JezJ3fglQYXR7A/exec"
    requests.get(gurl, params=payload)

# Meine gurl: "https://script.google.com/macros/s/AKfycbxf4_c6BEXWc-HQkD-AB1eZRRvoY5UahGAtvIfTGfJXVIetESzZ/exec"
# BasilsBot chat_id: 701987049


def sendToBasilsBot(msg, parseMode):
    telegramUrl = "https://api.telegram.org/bot1079228725:AAFBZd5qkfqkQC2Pm3UCj-wY90T0vmCUI6Y"
    newUrl = telegramUrl + "/sendMessage?chat_id=701987049&text=" + msg + "&parse_mode=" + parseMode
    requests.post(newUrl)
   

def sendToBoostBot(msg, parseMode):
    telegramUrl = "https://api.telegram.org/bot632005608:AAGkgrZBxk1fmKb2nTpx5jEENr6UacEsbKc"
    newUrl = telegramUrl + "/sendMessage?chat_id=-1001342120887&text=" + msg + "&parse_mode=" + parseMode
    requests.post(newUrl)


def corr_time(value):
    tday = datetime.now()
    bbDate = datetime.strptime(value, "%d/%m/%Y %H:%M")
    newdate = bbDate + timedelta(hours=2)
    
    return newdate.strftime("%d/%m/%Y %H:%M")


def fancy_time(uglyTimeString):
    uglyDate = datetime.strptime(uglyTimeString, "%d/%m/%Y %H:%M")
    tday = datetime.now()
    
    if uglyDate.day == tday.day:
        return "Heute " + uglyDate.strftime("%H:%M")
    elif uglyDate.day == tday.day+1:
        return "Morgen " + uglyDate.strftime("%H:%M")
    else:
        return uglyDateString



def getNextMatchesHtml(driver):

    url = 'https://www.betbrain.com/next-matches/'
    driver.get(url)
    time.sleep(5)

    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//form[@class="Form"]//input[@id="InputEmail"]'))
        )
    except Exception:
        driver.quit()
        sendToBasilsBot("LogInFindError", "Markdown")
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
            sendToBasilsBot("LogInInputError", "Markdown")
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
                sendToBasilsBot("FilterFindError", "Markdown")
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
                time.sleep(4)
            

                for x in range(70):
                    #rightnow = datetime.now().strftime("%x %X")
                    #print(rightnow + " - page " + str(x+1))
                    try:
                        mrebtnwt = WebDriverWait(driver, 6).until(
                            EC.presence_of_element_located((By.XPATH, '//button[@class="Button SportsBoxAll LoadMore"]'))
                        )
                    except Exception:
                        #rightnow = datetime.now().strftime("%x %X")
                        #print(rightnow +  " - break")
                        break
                    else:
                        try:
                            time.sleep(1)
                            mrebtn = driver.find_element_by_xpath('//button[@class="Button SportsBoxAll LoadMore"]')
                            time.sleep(0.5)
                            mrebtn.send_keys(Keys.RETURN)
                        except Exception:
                            #print("fail")
                            continue
                    finally:
                        time.sleep(1)

    finally:
        #print("no more")
        try:
            pups = WebDriverWait(driver, 3).until(                 EC.presence_of_element_located((By.XPATH, '//ul[@class="MatchesList"]'))                       )
        except Exception:
            #print("Error: ", sys.exc_info()[0])
            driver.quit()
            #print("MatchesListFindError")
            #sendToBasilsBot("MatchesListFindError", "Markdown")
            time.sleep(1)
            sys.exit()
        else:
            ulElem = driver.find_element_by_xpath('//ul[@class="MatchesList"]')
            time.sleep(2)
            try:
                htmldoc = ulElem.get_attribute('innerHTML')
                time.sleep(2)
            except Exception:
                driver.quit()
                sendToBasilsBot("GetAttributeError", "Markdown")
                time.sleep(1)
                sys.exit()
            else:
                # driver.close()
                try:
                    tree = html.fromstring(htmldoc)
                    time.sleep(2)
                except Exception:
                    driver.quit()
                    sendToBasilsBot("fromStringError", "Markdown")
                    time.sleep(1)
                    sys.exit()
                else:
                    #rightnow = datetime.now().strftime("%x %X")
                    #print(rightnow + " - First step successful")

                    return tree





def getGoodLinks(tree):

    linkList = []
    theGoodList = []

    for Match in tree.xpath("//li[@class='Match']"):

        for Quoten in Match.xpath(".//li[@class='Bet']"):
            try:
                Quote = float(Quoten.xpath(".//span[@class='Odds']/span[3]/text()")[0])
            except Exception:
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
                DaTiTimeHndrTemp = DaTi.split(" ")[1].split(":")
                DaTiTimeHndr = DaTiTimeHndrTemp[0] + DaTiTimeHndrTemp[1]
                
                MatchDate = DaTi.split(" ")[0]
                MatchHour = DaTi.split(" ")[1].split(":")[0]
                MatchMin = DaTi.split(" ")[1].split(":")[1]
                MatchTimeHndr = int(MatchHour + MatchMin)
                rnTimeHndr = int(rightnowStart)
                
                if Bookie in BookiesOhneSteuer:
                    Ratio = round((Quote * globalazq / AVG), 2)
                else:
                    Ratio = round((Quote * globalazq * globaltax / AVG), 2)

                if Ratio > grenzratio and AVG <= grenzavg and MatchLink not in linkList and ((MatchDate == todayDate and MatchTimeHndr > rnTimeHndr) or MatchDate != todayDate):
                    linkList.append(MatchLink)
                    theGoodList.append([HomeTeam, AwayTeam, DaTi, MatchLink])

                    #print(Bookie, HomeTeam, HDA, Ratio, Quote, AVG)

    # print([linkList, homeTeamList, awayTeamList, dateTimeList])

    return [linkList, theGoodList]



def getSingleMatchHtml(driver, url):
    
    try:
        driver.get(url)
    except Exception:
        #rightnow = datetime.now().strftime("%x %X")
        #print(rightnow + " GetSinglePageError")
        #sendToBasilsBot("GetSinglePageError")
        return None
    else:
        time.sleep(3)
        try:
            tableElem = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="OTBookmakers"]/parent::*'))
            )
        except Exception:
            # sendToBasilsBot("FindBookmakersTableError", "Markdown")
            #print("FindBookmakersTableError " + url)
            return None
        else:
            try:
                htmldoc = tableElem.get_attribute('innerHTML')
                time.sleep(0.5)
            except Exception:
                #print("GetAttributeError2")
                return None
            else:
                try:
                    tree = html.fromstring(htmldoc)
                    time.sleep(0.5)
                except Exception:
                    #print("fromStringError2")
                    return None
                else:
                    #rightnow = datetime.now().strftime("%x %X")
                    #print(rightnow + " got single page")
                    
                    return tree



def getBookiesList(tree):

    bookiesList = []

    for bookieLine in tree.xpath('.//li[contains(@class,"OTBookieContainer")]'):

        try: 

            bookie = bookieLine.xpath('.//span[@class="BookieLogo BL"]/span/text()')[0]
        except Exception:
            #print("FAIL: bookie = " + bookie)
            bookie = "Pups"
        else:
            bookiesList.append(bookie)

    return bookiesList



def getOddsListPerBookie(oddsRow):

    oddsListPerBookieTemp =[]
    oddsListPerBookie = [1,1,1]

    for oddsField in oddsRow:
        try:
            odd = float(oddsField.xpath('./a/span/span/text()')[0])

        except Exception:
            oddsListPerBookieTemp.append(1)

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
    avgList = [999,999,999]

    for avgField in tree.xpath('.//div[@class="OTBookmakersStatsOdds"]/ul[1]/li[@class="OTCol IsAverage"]'):
        try:
            avg = float(avgField.xpath('./text()')[0])

        except Exception:
            avgListTemp.append(999)

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



def getRatio(quoten, avgs, bookie):
    ratios = []
    steuerFaktor = 0.95
    if bookie in BookiesOhneSteuer:
        steuerFaktor = 1
        
    if avgs[1] == 999:
        avgDraw = 0
    else:
        avgDraw = 1/avgs[1]
        
    azq = round(1 / ( 1/avgs[0] + avgDraw + 1/avgs[2] ), 3)

    for k in range(3):
        try:
            ratioTemp = round((quoten[k] * azq * steuerFaktor / avgs[k]), 2)
            ratios.append(ratioTemp)
        except Exception:
            sendToBasilsBot("RatioCalcError: " + bookie + ", " + str(quoten[k]) + ", " + str(avgs[k]) + ", " + str(azq), "Markdown")
            ratios.append(0.2)            

    return ratios




def getDemNumbers(tree, avgs):

    oddsListTotal = []
    listComplete = []

    bookiesList = getBookiesList(tree)

    oddsRows = tree.xpath('.//ul[@class="OTRow"]')

    for i in range(len(bookiesList)):
        oddsListPerBookie = getOddsListPerBookie(oddsRows[i])
        oddsListTotal.append(oddsListPerBookie)

    for row in range(len(bookiesList)):
        quoten = oddsListTotal[row]
        bookie = bookiesList[row]
        
        ratios = getRatio(quoten, avgs, bookie)

        listComplete.append([bookiesList[row], quoten, ratios])
        # print([bookiesList[row], quoten, ratios])

    return listComplete





# ++++++++++++ GET LIVESCORES +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




def getLiveMatchesList(duplesMatches):
    
    # duplesMatch = HomeTeam + " vs. " + AwayTeam + "," + DaTi + "," + MatchLink + "," + HDA + "," + Bookie + ",pre,\n"
    
    liveMatchesList = []
    
    for i in range(len(duplesMatches)):
        line = duplesMatches[i]
        lineTeams = line.split(",")[0]
        lineStatus = line.split(",")[5]
        if lineStatus == "post":
            continue
        lineLink = line.split(",")[2]
        
        lineDate = line.split(",")[1].split(" ")[0]
        lineHour = line.split(",")[1].split(" ")[1].split(":")[0]
        lineMin = line.split(",")[1].split(" ")[1].split(":")[1]
        lineTimeHndr = int(lineHour + lineMin)
        lineTimeThreeHrsLater = lineTimeHndr + 400
        if lineTimeThreeHrsLater > 2400:
            lineTimeThreeHrsLater -= 2400
        rnTimeHndr = int(rightnowStart)
        
        if lineDate == todayDate and rnTimeHndr >= lineTimeHndr and rnTimeHndr <= lineTimeThreeHrsLater or rightnowStart == "0500":
            liveMatchesList.append([lineTeams, line.split(",")[1], lineLink, line.split(",")[3], line.split(",")[4], i])
            #print(lineTeams, line.split(",")[1], lineLink, line.split(",")[3], line.split(",")[4], i)
            
    return liveMatchesList



def getLiveTreeFromBB(driver, liveMatchUrl): 
    
    try:
        driver.get(liveMatchUrl)
    except Exception:
        return None
    else:
        time.sleep(4)
        #rightnow = datetime.now().strftime("%x %X")
        #print(rightnow + " - get new Live tree")        
                
        try:
            ScoresWrapperElem = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"ScoresContentWrapper")]'))
            )
        except Exception:
            #print("ERROR 1")
            sendToBasilsBot("GetLiveTreeError", "Markdown")
        else:
            try:
                ScoresWrapper = driver.find_element_by_xpath('//div[contains(@class,"ScoresContentWrapper")]')
                htmldoc = ScoresWrapper.get_attribute('innerHTML')
                time.sleep(1)
            except Exception:
                #print("ERROR 2")
                sendToBasilsBot("GetLiveTreeError", "Markdown")
            else:
                try:
                    tree = html.fromstring(htmldoc)
                    time.sleep(2)
                except Exception:
                    #print("ERROR 3")
                    sendToBasilsBot("GetLiveTreeError", "Markdown")
                else:
                    return tree
                
                
                
def getLiveScores(tree):
    
    rnTimeHndr = int(rightnowStart)
    scores = ""
    
    try:
        score1 = tree.xpath('.//span[@class="ScoresData"]/span[contains(@class,"ScoresHomeData")]/text()')[0]
        score2 = tree.xpath('.//span[@class="ScoresData"]/span[contains(@class,"ScoresAwayData")]/text()')[0]
        scores = score1 + ":" + score2
    except Exception:
        #print("Error: ", sys.exc_info()[0])
        try:
            for scoreField in tree.xpath('.//span[@class="ScoresPartialsLong"]/div'):
                for singleScoreField in scoreField.xpath('./span'):
                    scores += singleScoreField.xpath('./text()')[0]
        except Exception:
            #print("Error: ", sys.exc_info()[0])
            scores = "n/a"
            matchTime = "n/a"
    else:
        try:
            matchTimeTemp = tree.xpath('.//span[@class="ScoresDateWrapper"]/span[@class="ScoresDate"]/text()')[0]
        except Exception:
            #print("ERROR 4")
            pass
        else:
            if matchTimeTemp == "FINAL SCORE":
                matchTime = "FT"
            else:
                matchTime = matchTimeTemp.replace("LIVE | ", "")
    finally:
        return [scores, matchTime]
    



def getMsgForBot(data):
    # data = [HomeTeam, AwayTeam, DaTi, MatchLink, HDA, Bookie, Ratio, Quote, AVG, Sport, Country, Tour]
    
    rightnow = datetime.now().strftime("%x %X")
    #print(rightnow + data[0] + " not in dupelines")    
    
    msg = ("_Bookie:_ *" + data[5] +
        "*%0A%0A*" + data[0] + " vs. " + data[1] +
        "*%0A%0A_Time:_  " + fancy_time(data[2]) +
        "%0A_Sport:_  " + data[9] +
        "%0A_in:_  " + data[10] + ": " + data[11] +
        "%0A%0A_Wette:_     [" + data[4] + "](" + data[3].split("#")[0] +
        ")%0A_Ratio:_      *" + str(data[6]) +
        "*%0A_Quote:_     *" + str(data[7]) +
        "*%0A_avg:_         " + str(data[8]))
        
    return msg
  
  
  
  
  


## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++









#rightnow = datetime.now().strftime("%x %X")
#print(rightnow + " - starting")




driver = webdriver.Firefox(options=options)
time.sleep(2)




nmTree = getNextMatchesHtml(driver)

goodLinks = getGoodLinks(nmTree)
linkList = goodLinks[0]
goodLinksList = goodLinks[1]        # [HomeTeam, AwayTeam, DaTi, MatchLink]


#rightnow = datetime.now().strftime("%x %X")
#print(rightnow + " - linkList length: " + str(len(linkList)))



for b in range(len(goodLinksList)):
    
    smTree = getSingleMatchHtml(driver, linkList[b])   # tree
    
    time.sleep(1)
    
    if smTree is not None:
        #rightnow = datetime.now().strftime("%x %X")
        #print(rightnow + " - got match html #" + str(b+1))
        
        spiel = goodLinksList[b]
        averages = getAvg(smTree)
        numbersPerMatch = getDemNumbers(smTree, averages)
        # numbersPerMatch: [bookie, quoten, ratios, azq]

        theFinalObject = {
            "HomeTeam": spiel[0],
            "AwayTeam": spiel[1],
            "DaTi": spiel[2],
            "MatchLink": spiel[3],
            "Sport": spiel[3].split('#')[0].split("/")[3],
            "Country": spiel[3].split('#')[0].split("/")[4],
            "Tour": spiel[3].split('#')[0].split("/")[5],
            "AVG": averages,
            "Odds": numbersPerMatch,
            }


        for row in theFinalObject["Odds"]:

            for n in range(3):
                Bookie = row[0]
                Ratio = row[2][n]
                HomeTeam = theFinalObject["HomeTeam"]
                AwayTeam = theFinalObject["AwayTeam"]
                if n == 0:
                    HDA = "Home"
                elif n == 1:
                    HDA = "Draw"
                else:
                    HDA = "Away"
                DaTi = theFinalObject["DaTi"]
                MatchLink = theFinalObject["MatchLink"].split("#")[0]
                Quote = row[1][n]
                AVG = theFinalObject["AVG"][n]
                Sport = theFinalObject["Sport"]
                Country = theFinalObject["Country"]
                Tour = theFinalObject["Tour"]
                
                checkvar = HomeTeam + " vs. " + AwayTeam + "," + DaTi + "," + MatchLink + "," + HDA + "," + Bookie + ",pre,\n"
                
                f = open("/home/basil/Dokumente/MilkMachine/duples.txt", "r")
                dupelines = f.readlines()
                f.close()
                
                fb = open("/home/basil/Dokumente/MilkMachine/duples2.txt", "r")
                dupelinesBasil = fb.readlines()
                fb.close()
                    
                if Ratio > grenzratio and Bookie in activeBookies and checkvar not in dupelines:
                    
                    msgForBot = getMsgForBot([HomeTeam, AwayTeam, DaTi, MatchLink, HDA, Bookie, Ratio, Quote, AVG, Sport, Country, Tour])
                    sendToBoostBot(msgForBot, "Markdown")
                    
                    f2 = open("/home/basil/Dokumente/MilkMachine/duples.txt", "w")
                    for line in dupelines[1:]:
                        f2.write(line)
                    f2.write(checkvar)
                    f2.close()
                    
                    time.sleep(0.5)
                    
                elif Ratio > grenzratio2 and Bookie in basilsBookies and checkvar not in dupelinesBasil:
                    
                    msgForBot = getMsgForBot([HomeTeam, AwayTeam, DaTi, MatchLink, HDA, Bookie, Ratio, Quote, AVG, Sport, Country, Tour])
                    sendToBasilsBot(msgForBot, "Markdown")
                    
                    f2 = open("/home/basil/Dokumente/MilkMachine/duples2.txt", "w")
                    for line in dupelinesBasil[1:]:
                        f2.write(line)
                    f2.write(checkvar)
                    f2.close()
                    
                    time.sleep(0.5)


#rightnow = datetime.now().strftime("%x %X")
#print(rightnow + " - starting LIVE function")






# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++








#f8 = open("/home/basil/Dokumente/MilkMachine/duples.txt", "r")
#duplesMatches = f8.readlines()
#f8.close()

#liveMatchesList = getLiveMatchesList(duplesMatches)
## liveMatchesList: [lineTeams, DaTi, lineLink, HDA, bookie, i]


##rightnow = datetime.now().strftime("%x %X")
##print(rightnow + " - liveMatchesList length: " + str(len(liveMatchesList)))

## liveMatchesList: [Teams, DaTi, Link, HDA, Bookie, Status, lineTimeHndr, i]
## scores: [scores, matchTime]
## checkvar = HomeTeam + " vs. " + AwayTeam + "," + DaTi + "," + MatchLink + "," + HDA + "," + Bookie + ",pre,\n"




#for liveMatch in liveMatchesList:
    #liveTree = getLiveTreeFromBB(driver, liveMatch[2])
    ##rightnow = datetime.now().strftime("%x %X")
    ##print(rightnow + " - got another LIVE match html")
    #scores = getLiveScores(liveTree)
    
    #msgToSheet = {
        #"TeamsVar": liveMatch[0],
        #"ScoresVar": scores[0],
        #"TimesVar": scores[1]
    #}
    #sendToGoogle(msgToSheet)
    #print(liveMatch[0] + ", " + scores[0] + ", " + scores[1])
    
    #if scores[1] == "FT":
        #duplesMatches[liveMatch[5]] = liveMatch[0] + "," + liveMatch[1] + "," + liveMatch[2] + "," + liveMatch[3] + "," + liveMatch[4] + "," + "post,\n"
    
    #time.sleep(3)
        
driver.quit()

#f9 = open("/home/basil/Dokumente/MilkMachine/duples.txt", "w")
#for line in duplesMatches:
    #f9.write(line)
#f9.close()

if rightnowStart in chckpnts:
    sendToBasilsBot("- still running -", "Markdown")
        
#rightnow = datetime.now().strftime("%x %X")
#print(rightnow + " - finally done")
