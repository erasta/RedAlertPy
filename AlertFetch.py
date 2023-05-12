from bs4 import BeautifulSoup, NavigableString, Tag
import requests
from datetime import datetime
import re


def obtainLastAlerts():
    resp = requests.get("https://t.me/s/PikudHaOref_all")
    bs = BeautifulSoup(resp.text, features="lxml")
    # print(bs.get_text())
    divs = bs.find_all("div", {"class": "tgme_widget_message_text"})
    alerts = []
    for onediv in divs:
        # print('===>')
        filtered = [t for t in onediv if (not isinstance(t, NavigableString))]
        items = [t.get_text().strip() for t in filtered if t.get_text().strip() != ""]
        if len(items) > 1 and items[0] == "🚨":  # and 'ירי רקטות וטילים' in items[1]:
            remove_items = [
                "🚨",
                "https://www.oref.org.il/12761-he/Pakar.aspx",
                "להנחיות המלאות -",
            ]
            items = [t for t in items if t not in remove_items]
            timeitems = [t for t in items if re.search(r"[\[\]/:]", t)]
            if len(timeitems) > 0:
                pos = timeitems[0].index("[")
                dt = datetime.strptime(timeitems[0][pos:], "[%d/%m/%Y] %H:%M")
                items = [t for t in items if t != timeitems[0]]
                items.insert(0, timeitems[0][:pos])
                info = [str(dt)] + items
                alerts.append(info)
                # print('===>', str(info))
    return alerts


def findNew(knownAlerts, gotAlerts):
    newAlerts = []
    for a in gotAlerts:
        found = False
        for old in knownAlerts:
            if "||".join(a) == "||".join(old):
                found = True
                break
        if not found:
            newAlerts.append(a)
    return newAlerts


def readOldAlerts():
    knownAlerts = []
    try:
        with open("old_alerts.txt", "r") as fin:
            for line in fin:
                a = line.strip().split("||")
                knownAlerts.append(a)
    except:
        pass
    return knownAlerts


if __name__ == "__main__":
    for a in obtainLastAlerts():
        print(a)
    # resp = requests.get("https://t.me/s/PikudHaOref_all")
    # bs = BeautifulSoup(resp.text, features="lxml")
    # divs = bs.find_all("div", {"class": "tgme_widget_message_text"})
    # for onediv in divs:
    #     print(onediv)
