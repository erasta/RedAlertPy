from datetime import datetime
import os
import time
from mastodon import Mastodon
import json
from Alert import Alert
from PlacesImageCreator import PlacesImageCreator


class MastoAlerts:
    def __init__(self) -> None:
        secrets = json.load(open("secrets.json"))
        self.mastodon = Mastodon(
            client_id=secrets["client_id"],
            client_secret=secrets["client_secret"],
            access_token=secrets["access_token"],
            api_base_url="https://" + secrets["mastodon_hostname"],
        )
        self.imageCreator = PlacesImageCreator()

    def fetch_toots(self):
        toots = self.mastodon.account_statuses(self.mastodon.me())
        analyzed = [Alert().from_toot(t.content) for t in toots]
        return analyzed

    def filter_new_alerts_by_toots(self, alerts, toot_alerts=None):
        toot_alerts = toot_alerts or self.fetch_toots()
        new_alerts = [a for a in alerts if not a.is_in_list(toot_alerts)]
        return new_alerts

    def post_alert(self, one_alert: Alert, actually_do_posts=False):
        print()
        start = datetime.now()

        fig = self.imageCreator.places_to_image(one_alert.places(), add_title=False)

        print("create image:", datetime.now() - start)

        os.makedirs("images", exist_ok=True)
        # image_name = "images/a" + str(datetime.now()) + ".png"
        image_name = "images/a.png"
        self.imageCreator.savefig(fig, image_name)

        print("save image:", datetime.now() - start)

        if actually_do_posts:
            media_dict = self.mastodon.media_post(image_name, "image/png")
            self.mastodon.status_post(
                one_alert.text(), in_reply_to_id=None, visibility="unlisted", media_ids=[media_dict]
            )
            print("posted: " + one_alert.show() + '\n' + one_alert.show_places())
        else:
            print("not posted: " + one_alert.show() + '\n' + one_alert.show_places())


if __name__ == "__main__":
    from AlertFetch import AlertFetch

    print("\nfeed:")
    toot_alerts = MastoAlerts().fetch_toots()
    for t in toot_alerts:
        print(t.show())
    print("\nsource:")
    alerts = AlertFetch().obtainNewAlerts()
    for a in alerts:
        print(a.show())
    print("\nnew:")
    for f in os.listdir("images"):
        os.remove("images/" + f)
    for a in MastoAlerts().filter_new_alerts_by_toots(alerts, toot_alerts):
        MastoAlerts().post_alert(a)
