import argparse
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

cur_date = datetime.now().strftime("%Y-%m")

parser = argparse.ArgumentParser("city")
parser.add_argument("city", help="Város meghatározása", type=str)
args = parser.parse_args()

city = args.city
url = f"https://www.idokep.hu/idojaras/{city}"

r = requests.get(url,verify=False)
soup = BeautifulSoup(r.text, "html.parser")
container = soup.find(class_="ik daily-forecast-container")
columns = container.find_all(class_="ik dailyForecastCol")

current_temp = soup.find(class_="ik current-temperature").text.strip()
current_text = soup.find(class_="ik current-weather").text.lower()
med_effect = soup.find_all(class_="pt-2")[3].text.strip()

days = []
minima = []
maxima = []
rains = []

for column in columns:
    try:
        day = column.find(class_="ik dfDayNum").text
    except AttributeError as ae:
        day = column.find(class_="ik dfDayNum vacation").text

    days.append(f"{cur_date}-{day}")
    temps = column.find(class_="ik min-max-container").find_all("a")
    minima.append(temps[0].text)
    maxima.append(temps[1].text)

    try:
        rainlevel = column.find(class_="ik rainlevel-container").text.strip()
    except AttributeError as ae:
        rainlevel = "-"

    rains.append(rainlevel)

print("*" * len(city))
print(f"{city}")
print("*" * len(city))
print()
print(
    f"""Jelenleg:
{current_temp} {current_text}
{med_effect}
"""
)
print("Előrejelzés")
print(
    tabulate(
        list(zip(days, maxima, minima, rains)),
        headers=["dátum", "min", "max", "csapadék"],
    )
)
