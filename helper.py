import os

fan_duel = 'https://il.sportsbook.fanduel.com/sports/navigation/830.1/10107.3'
draft_kings = 'https://sportsbook.draftkings.com//sites/US-SB/api/v1/eventgroup/103/full?includePromotions=true&format=json'
points_bet = 'https://il.pointsbet.com/sports/basketball/NBA'

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "driver/chromedriver_88")


def find_elem_by_content(content, elems):
    for elem in elems:
        if content in elem.text:
            return elem
