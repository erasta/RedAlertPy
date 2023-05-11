import time
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re

def obtainLastAlerts():
    resp = requests.get('https://t.me/s/PikudHaOref_all')
    bs = BeautifulSoup(resp.text, features="lxml")
    # print(bs.get_text())
    divs = bs.find_all("div", {"class": "tgme_widget_message_text"})
    alerts = []
    for onediv in divs:
        # print('===>')
        items = [t.get_text().strip() for t in onediv if t.get_text().strip() != '']
        if items[0] == '🚨': # and 'ירי רקטות וטילים' in items[1]:
            remove_items = ['🚨', 'https://www.oref.org.il/12761-he/Pakar.aspx', 'להנחיות המלאות -']
            items = [t for t in items if t not in remove_items]
            timeitems = [t for t in items if re.search(r'[\[\]/:]', t)]
            if len(timeitems) > 0: 
                pos = timeitems[0].index('[')
                dt = datetime.strptime(timeitems[0][pos:], '[%d/%m/%Y] %H:%M')
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
            if '||'.join(a) == '||'.join(old):
                found = True
                break
        if not found:
            newAlerts.append(a)
    return newAlerts

knownAlerts = []
while True:
    gotAlerts = obtainLastAlerts()
    newAlerts = findNew(knownAlerts, gotAlerts)
    if len(newAlerts) > 0:
        print(datetime.now())
        for a in newAlerts:
            print(' '.join(a))
            knownAlerts.append(a)
    time.sleep(1)
    # print(a)