import requests
from bs4 import BeautifulSoup
from ports import scraper
import time

class Data(scraper.Data):
    def getScrapeResult():
        url = 'https://www.amazon.com/s?k=motorola'

        response = requests.get(
            url,
            headers={
                "User-Agent": "JonBot",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                # "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Priority": "u=0, i",
                },
        )

        # TODO: add caching so that we don't have to reload the data directly every time.


        # TODO: maybe add eponetial back off to repect rate limits, 
        # but right now its pointless because this request runs only once per run of the whole program.
        # 
        if (response.status_code == 429):
            print("sleeping")
            time.sleep(60) 

        soup = BeautifulSoup(response.text, 'html.parser')
        spots = soup.find_all("i", class_="a-icon-star-small")

        spotFields = []

        for spot in spots:
            top = spot.parent.parent.parent.parent.parent
            title = str(top.find(findH2Title).span.string)
            
            starRating = str(spot.contents[0].string)

            ratingsCount = str(top.find("span", class_="a-size-base s-underline-text").string)
        
            spotFields.append({
                "title": title,
                "starRating": starRating,
                "ratingsCount": ratingsCount,
            })

        return spotFields
    
def findH2Title(tag):
    return tag.name == "h2" and tag.has_attr("aria-label")