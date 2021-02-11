import requests
import json, time

from selenium.webdriver.remote.webelement import WebElement

from helper import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs


def spreads_draft_kings():
    spreads = dict()

    res = json.loads(requests.get(draft_kings).text)
    # filter out unused
    res = res['eventGroup']['offerCategories'][0]['offerSubcategoryDescriptors'][1]['offerSubcategory']['offers']

    for game in res:
        for spread in game:
            name1, name2 = spread['outcomes'][0]['participant'], spread['outcomes'][1]['participant']
            match_name = name1.split()[1] + ' v ' + name2.split()[1]
            if match_name not in spreads:
                spreads[match_name] = {
                    name1: dict(),
                    name2: dict()
                }

            spreads[match_name][name1][spread['outcomes'][0]['line']] = int(spread['outcomes'][0]['oddsAmerican'])
            spreads[match_name][name2][spread['outcomes'][1]['line']] = int(spread['outcomes'][1]['oddsAmerican'])

    return spreads


def spreads_points_bet():
    spreads = dict()

    driver = webdriver.Chrome(executable_path=DRIVER_BIN)
    driver.get(points_bet)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'mainContent'))
        )
    finally:
        soup = bs(driver.page_source, 'html.parser')
        urls = pb_game_urls(soup)

    for url in urls:
        driver.get(points_bet + url)
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'f1jdqmw8'))
            )
        finally:
            soup = bs(driver.page_source, 'html.parser')
            name1, name2 = soup.find_all("p", {"class": "f1jdqmw8"})[0].text, soup.find_all("p", {"class": "f1jdqmw8"})[1].text
            match_name = name1.split()[1] + ' v ' + name2.split()[1]

            spreads[match_name] = {
                name1: dict(),
                name2: dict()
            }

            buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Pick Your Own Spread')]")
            if buttons:
                btn = buttons[0].find_element_by_xpath('..')
                driver.execute_script("arguments[0].click();", btn)
                expand = driver.find_elements_by_class_name("fq7xcxd")[0]
                driver.execute_script("arguments[0].click();", expand)

                soup = bs(driver.page_source, 'html.parser')
                spreads_html = soup.find_all("div", {"class": "f8qvbex"})[0]
                name_lines = spreads_html.find_all("div", {"class": "f2dhou8"})
                odds = spreads_html.find_all("span", {"class": "fheif50"})

                for i in range(len(name_lines)):
                    name, line = split_name_line(name_lines[i].text)
                    spreads[match_name][name][float(line)] = int(odds[i].text)

    return spreads


def pb_game_urls(soup):
    res = []
    links = soup.find_all("a", {"class": "f1x4xdln"})
    for l in links:
        res.append('/' + l.get('href').split('/')[4])

    return res


def split_name_line(text):
    split_text = text.split()
    name = ""
    for i in range(len(split_text)-1):
        name += split_text[i] + " "

    return name[:-1], split_text[-1]


def main():
    print(spreads_draft_kings())
    print(spreads_points_bet())


if __name__ == "__main__":
    main()
