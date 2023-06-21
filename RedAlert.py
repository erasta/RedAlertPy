import argparse
import os
import time
from datetime import datetime
import traceback

from AlertFetch import AlertFetch
from MastoAlerts import MastoAlerts


class RedAlert:
    def __init__(self, actually_do_posts=False) -> None:
        self.actually_do_posts = actually_do_posts
        self.masto = MastoAlerts()
        self.fetcher = AlertFetch()

    def go(self):
        try:
            self.knownAlerts = self.masto.fetch_toots()
            lastTootsFetch = datetime.now()
            print("\npast:")
            for a in reversed(self.knownAlerts):
                print(a.show())
            while True:
                if (datetime.now() - lastTootsFetch).total_seconds() > 60:
                    self.knownAlerts = self.masto.fetch_toots()
                    lastTootsFetch = datetime.now()
                gotAlerts = self.fetcher.obtainNewAlerts()
                newAlerts = self.masto.filter_new_alerts_by_toots(gotAlerts, self.knownAlerts)
                if len(newAlerts) > 0:
                    print(datetime.now())
                    for a in newAlerts:
                        self.masto.post_alert(a, self.actually_do_posts)
                        self.knownAlerts.append(a)
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping by keyboard")
        except Exception as ex:
            print(f"Crush because of {type(ex).__name__}: {ex}")  # , ''.join(traceback.format_exception(e)))
            self.masto.mastodon.status_post(
                f"Crush because of {type(ex).__name__}: {ex}", in_reply_to_id=None, visibility="unlisted"
            )
            raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--posts", action="store_true")
    args = parser.parse_args()
    print(args)

    if os.path.isdir("images"):
        for f in os.listdir("images"):
            os.remove("images/" + f)

    RedAlert(args.posts).go()
