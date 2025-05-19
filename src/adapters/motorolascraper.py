import time
import csv
import io

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from ports import scraper


class ItemFindException(Exception):
    """Thrown when an scrape item raises an exception while using soup find."""


class URLRequestException(Exception):
    """Thrown when a URL request raises an Exception."""


class Data(scraper.Data):
    def get_scrape_result(self=None):

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
            page_source = with_retry(url, 1)
            items += extract_from_page_source(page_source)

        # TODO: get ratings and descriptions after the requests are handled better so that they don't take so long to run.
        # for item in items:
        #     itemPageSource = make_request(item["link"], "bv_rating_content2", "scroll")
        #     resultText = extract_ratings_from_page_source(itemPageSource)
        #     item["rating"] = resultText[0]
        #     item["ratings count"] = resultText[1]

        return items


def with_retry(url, tries):
    try:
        result = make_request(url, "moto_dlp_products_item_content", "wait")
    except TimeoutException:
        if tries == 0:
            return ""
        tries -= tries
        result = with_retry(url, tries)
    return result


def make_request(url, wait_class_name, mode="wait"):
    # self imposed rate limit
    time.sleep(1)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
    )

    # service = webdriver.ChromeService(log_output="")
    service = webdriver.ChromeService()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)

        if mode == "wait":
            wait(driver, wait_class_name, 3)
        else:
            scroll(driver, 1)
    except TimeoutException as exc:
        raise TimeoutException(
            f"Timeout waiting for element {wait_class_name} on {url}"
        ) from exc
    except NoSuchElementException as exc:
        raise NoSuchElementException(
            f"Element {wait_class_name} not found on {url}"
        ) from exc
    except Exception as e:
        raise URLRequestException(f"An error occurred: {str(e)} on {url}") from e

    return driver.page_source


def wait(driver, wait_class_name, seconds=10):
    WebDriverWait(driver, seconds).until(
        EC.presence_of_element_located((By.CLASS_NAME, wait_class_name))
    )


def scroll(driver, sleep_seconds=1):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(sleep_seconds)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def extract_from_page_source(page_source):
    soup = BeautifulSoup(page_source, "html.parser")

    items = soup.find_all(class_="moto_dlp_products_item_content")

    item_fields = []

    for item in items:
        title = ""
        try:
            title = (
                str(item.find(class_="moto_dlp_products_item_content_name").string)
                + " "
                + str(item.find(class_="moto_dlp_products_item_content_color").string)
            )
            price = str(tag_as_string(item.find(find_final_price)))
            link = str(item.find(find_link)["href"])
        except Exception as e:
            raise ItemFindException(f"title: {title}, error: {str(e)}") from e

        item_fields.append(
            {
                "title": title,
                "price": price,
                "link": "https://www.motorola.com" + link,
            }
        )

    return item_fields


def extract_ratings_from_page_source(page_source):
    soup = BeautifulSoup(page_source, "html.parser")

    ratings = soup.find("bv_rating_content2")

    return [
        str(tag_as_string(follow(ratings, ["section", "div", "div", "div"]))),
        str(tag_as_string(follow(ratings, ["section", "div", "div", "button", "div"]))),
    ]


def follow(tag, searchkeys):
    if tag is None or tag == "":
        return ""
    if len(searchkeys > 1):
        return follow(tag.find(searchkeys[0]), searchkeys[1, len(searchkeys) - 1])
    if len(searchkeys) == 1:
        return tag.find(searchkeys[0])
    return ""


def tag_as_string(tag):
    if tag is None or tag == "":
        return ""
    return tag.string


def find_final_price(tag):
    return (
        tag.name == "div"
        and tag.has_attr("aria-label")
        and tag["aria-label"] == "FinalPrice"
    )


def find_link(tag):
    return (
        tag.name == "a"
        and tag.has_attr("data-action")
        and tag["data-action"] == "Buy Now"
    )
