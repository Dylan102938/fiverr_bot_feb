import requests
import json
from helper import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs


def ml_draft_kings():
    res = json.loads(requests.get(draft_kings).text)

    # filter out unused
    res = res['eventGroup']['offerCategories'][0]['offerSubcategoryDescriptors'][0]['offerSubcategory']['offers']

    games = dict()
    for game in res:
        first_team, second_team = game[2]['outcomes'][0]['participant'], game[2]['outcomes'][1]['participant']
        first_team_ml, second_team_ml = game[2]['outcomes'][0]['oddsAmerican'], game[2]['outcomes'][1]['oddsAmerican']

        games[first_team.split()[1] + ' v ' + second_team.split()[1]] = {
            'name1': first_team,
            'name2': second_team,
            'money_line1': int(first_team_ml),
            'money_line2': int(second_team_ml)
        }

    return games


def ml_points_bet():
    games = dict()

    driver = webdriver.Chrome(executable_path=DRIVER_BIN)
    driver.get(points_bet)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'mainContent'))
        )
    finally:
        soup = bs(driver.page_source, 'html.parser')

        games_html = soup.findAll("div", {"class": "f12moq1z"})
        for game_html in games_html:
            ml_id = len(game_html.findAll("span", {"class": "fnapeds"}))

            game_names_html = game_html.find_all("p", {"class": "fji5frh"})
            name1, name2 = game_names_html[0].text, game_names_html[1].text

            game_ml_html = game_html.find_all("span", {"class": "fheif50"})
            ml1, ml2 = game_ml_html[ml_id-1].text, game_ml_html[2*ml_id-1].text

            games[name1.split()[1] + ' v ' + name2.split()[1]] = {
                'name1': name1,
                'name2': name2,
                'money_line1': int(ml1),
                'money_line2': int(ml2)
            }

        return games


def ml_fan_duel():
    games = dict()

    driver = webdriver.Chrome(executable_path=DRIVER_BIN)
    driver.get(fan_duel)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'coupon-event'))
        )
    finally:
        soup = bs(driver.page_source, 'html.parser')

        games_html = soup.findAll("div", {"class": "coupon-event"})
        for game_html in games_html:
            game_names_html = game_html.find_all("span", {"class": "name"})
            name1, name2 = game_names_html[0].text, game_names_html[1].text

            game_ml_html = game_html.find_all("div", {"class": "selectionprice"})
            ml1, ml2 = game_ml_html[2].text, game_ml_html[3].text

            games[name1.split()[1] + ' v ' + name2.split()[1]] = {
                'name1': name1,
                'name2': name2,
                'money_line1': int(ml1),
                'money_line2': int(ml2)
            }

        return games


def main():
    print(ml_draft_kings())
    print(ml_fan_duel())
    print(ml_points_bet())


if __name__ == "__main__":
    main()