from datetime import datetime
from mastodon import Mastodon
import json


class MastoAlerts:
    def __init__(self) -> None:
        secrets = json.load(open("secrets.json"))
        self.mastodon = Mastodon(
            client_id = secrets["client_id"],
            client_secret = secrets["client_secret"],
            access_token = secrets["access_token"],
            api_base_url = 'https://' + secrets["mastodon_hostname"],
        )

    def fetch_toots(self):
        toots = self.mastodon.account_statuses(self.mastodon.me())
        toots = [t.content.replace('<br />', '||').replace('<p>', '').replace('</p>', '').strip().split('||') for t in toots]
        # print(json.dumps(toots[0], indent=2, default=lambda x: str(x) if type(x) is datetime else x))
        # print('\nfeed:')
        # for t in toots:
        #     print(' '.join(t).strip())
        return toots

    def filter_new_alerts_by_toots(self, alerts, toots=None):
        if toots is None:
            toots = self.fetch_toots()
        new_alerts = []
        for a in alerts:
            if ' '.join(a).strip() not in [' '.join(t).strip() for t in toots]:
                new_alerts.append(a)
                # print(' '.join(a).strip())
        return new_alerts

    def post_alert(self, one_alert):
        toot_text = '\n'.join(one_alert).strip()
        self.mastodon.status_post(toot_text, in_reply_to_id=None, visibility='unlisted')
        print('posted: ' + ' '.join(one_alert).strip())


if __name__ == '__main__':
    from AlertFetch import obtainLastAlerts
    print('\nfeed:')
    for t in MastoAlerts().fetch_toots():
        print(' '.join(t).strip())
    alerts = obtainLastAlerts()
    print('\nsource:')
    for a in alerts:
        print(' '.join(a).strip())
    print('\nnew:')
    for a in MastoAlerts().filter_new_alerts_by_toots(alerts):
        print(' '.join(a).strip())

