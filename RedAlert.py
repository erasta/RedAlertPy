import time
from datetime import datetime
from mastodon import Mastodon
import json

from AlertFetch import *

secrets = json.load(open("secrets.json"))
mastodon = Mastodon(
    client_id = secrets["client_id"],
    client_secret = secrets["client_secret"],
    access_token = secrets["access_token"],
    api_base_url = 'https://' + secrets["mastodon_hostname"],
)

knownAlerts = readOldAlerts()
print('old')
for a in knownAlerts:
    print(' '.join(a))

while True:
    gotAlerts = obtainLastAlerts()
    newAlerts = findNew(knownAlerts, gotAlerts)
    if len(newAlerts) > 0:
        print(datetime.now())
        with open("old_alerts.txt", "a") as fout:
            for a in newAlerts:
                print(' '.join(a))
                knownAlerts.append(a)
                fout.write('||'.join(a) + '\n')
                toot_text = '\n'.join(a)
                # print(toot_text)
                mastodon.status_post(toot_text, in_reply_to_id=None, visibility='unlisted')
    time.sleep(1)

