import traceback
from bs4 import BeautifulSoup, NavigableString, Tag
import requests
from datetime import datetime
import re

from Alert import Alert


class AlertFetch:
    def obtainNewAlerts(self):
        alerts: list[Alert] = []
        try:
            resp = requests.get("https://t.me/s/PikudHaOref_all")
            bs = BeautifulSoup(resp.text, features="lxml")
            # print(bs.get_text())
            divs = bs.find_all("div", {"class": "tgme_widget_message_text"})
            for onediv in divs:
                # print('===>', onediv)
                filtered = [t for t in onediv]  # if (not isinstance(t, NavigableString))]
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
                        alerts.append(Alert(info))
                        # print('===>', str(info))
        except requests.ConnectionError as ex:
            msg = f"Got error {type(ex).__name__}: {ex}\n{''.join(traceback.format_exc())}"
            if self.last_error != msg:
                print(msg)
                self.last_error = msg
        return alerts


if __name__ == "__main__":
    for a in AlertFetch().obtainNewAlerts():
        print(a)
