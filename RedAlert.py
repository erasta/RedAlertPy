import argparse
import os
import sys
import time
from datetime import datetime
from Alert import Alert

from AlertFetch import AlertFetch
from MastoAlerts import MastoAlerts


class RedAlert:
    def __init__(self, actually_do_posts=False) -> None:
        self.actually_do_posts = actually_do_posts
        self.masto = MastoAlerts()
        self.fetcher = AlertFetch()

    def go(self):
        self.knownAlerts = self.masto.fetch_toots()
        print("\npast:")
        for a in reversed(self.knownAlerts):
            print(a.show())
        while True:
            gotAlerts = self.fetcher.obtainNewAlerts()
            newAlerts = self.masto.filter_new_alerts_by_toots(gotAlerts, self.knownAlerts)
            if len(newAlerts) > 0:
                print(datetime.now())
                for a in newAlerts:
                    self.masto.post_alert(a, self.actually_do_posts)
                    self.knownAlerts.append(a)
            time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--posts", action="store_true")
    args = parser.parse_args()
    print(args)

    for f in os.listdir("images"):
        os.remove("images/" + f)

    RedAlert(args.posts).go()
