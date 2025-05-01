from bs4 import BeautifulSoup
from ports import scraper
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

class Data(scraper.Data):
    def getScrapeResult():

        urls = [
            "https://www.motorola.com/us/en/family/razr.html",
            "https://www.motorola.com/us/en/family/edge.html",
            "https://www.motorola.com/us/en/family/g.html",
            "https://www.motorola.com/us/en/specials.html",
            "https://www.motorola.com/us/en/family/all-cases-and-protection.html",
            "https://www.motorola.com/us/en/family/headphones.html",
            "https://www.motorola.com/us/en/family/wearables.html",
            "https://www.motorola.com/us/en/family/power-and-charger.html",
            "https://www.motorola.com/us/en/family/auto-accessories.html",
            "https://www.motorola.com/us/en/family/security-surveillance.html",
            "https://www.motorola.com/us/en/family/modems-networking.html",
            "https://www.motorola.com/us/en/family/home-office-phones.html",
            "https://www.motorola.com/us/en/smartphones/index.html",
            # "https://www.motorola.com/us/en/p/pg38c06068",
            # "https://www.motorola.com/us/en/p/phones/razr/razr-plus-gen-2/pmipmgs38mh?pn=PB2J0014US",
            # "https://www.motorola.com/us/en/p/phones/motorola-edge/edge-plus-gen-3/pmipmfo33m2?pn=PAWJ0002US",
        ]

        items = []

        for url in urls:
            pageSource = withRetry(url, 1)
            items += extractFromPageSource(pageSource)

        # TODO: get ratings and descriptions after the requests are handled better so that they don't take so long to run.
        # for item in items:
        #     itemPageSource = makeRequest(item["link"], "bv_rating_content2", "scroll")
        #     resultText = extractRatingsFromPageSource(itemPageSource)
        #     item["rating"] = resultText[0]
        #     item["ratings count"] = resultText[1]

        return items
        
def makeRequest(url, waitClassName, mode="wait"):
    # self imposed rate limit
    time.sleep(1)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36")

    # service = webdriver.ChromeService(log_output="")
    service = webdriver.ChromeService()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        
        if (mode == "wait"):
            wait(driver, waitClassName, 3)
        else:
            scroll(driver, 1)
    except TimeoutException:
        raise Exception(f"Timeout waiting for element {waitClassName} on {url}")
    except NoSuchElementException:
        raise Exception(f"Element {waitClassName} not found on {url}")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)} on {url}")

    return driver.page_source

def wait(driver, waitClassName, seconds=10):
    WebDriverWait(driver, seconds).until(
        EC.presence_of_element_located((By.CLASS_NAME, waitClassName))
    )

def scroll(driver, sleepSeconds=1):
    last_height = driver.execute_script("return document.body.scrollHeight")
            
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(sleepSeconds)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extractFromPageSource(pageSource):
        soup = BeautifulSoup(pageSource, 'html.parser')

        items = soup.find_all(class_="moto_dlp_products_item_content")
        
        itemFields = []

        for item in items:
            try:
                title = str(item.find(class_="moto_dlp_products_item_content_name").string) + " " + str(item.find(class_="moto_dlp_products_item_content_color").string)
                price = str(TagAsString(item.find(findFinalPrice)))
                link = str(item.find(findLink)["href"])                                                                   
            except Exception as e:
                raise Exception(f"title: {title}, error: {str(e)}")

            itemFields.append({
                "title": title,
                "price": price,
                "link": "https://www.motorola.com"+link,
            })

        return itemFields

def extractRatingsFromPageSource(pageSource):
    soup = BeautifulSoup(pageSource, 'html.parser')
    
    ratings = soup.find("bv_rating_content2")
    
    return [str(TagAsString(follow(ratings, ["section", "div", "div", "div"]))), str(TagAsString(follow(ratings, ["section","div","div","button","div"])))]

def withRetry(url, tries):
    try:
        result = makeRequest(url, "moto_dlp_products_item_content", "wait")
    except TimeoutException:
        if (tries == 0):
            return ""
        tries -= tries
        result = withRetry(tries)
    return result

def follow(tag, searchkeys):
    if (tag is None or tag == ""):
        return ""
    if (len(searchkeys > 1)):
        return follow(tag.find(searchkeys[0]), searchkeys[1, len(searchkeys)-1])
    if (len(searchkeys) == 1):
        return tag.find(searchkeys[0])
    return ""

def TagAsString(tag):
    if (tag is None or tag == ""):
        return ""
    return tag.string

def findFinalPrice(tag):
    return tag.name == "div" and tag.has_attr("aria-label") and tag["aria-label"] == "FinalPrice"

def findLink(tag):
    return tag.name == "a" and tag.has_attr("data-action") and tag["data-action"] == "Buy Now"