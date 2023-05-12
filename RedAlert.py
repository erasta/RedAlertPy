import time
from datetime import datetime
from mastodon import Mastodon
import json

from AlertFetch import *
from MastoAlerts import MastoAlerts

masto = MastoAlerts()
knownAlerts = masto.fetch_toots()
print('\npast:')
for a in reversed(knownAlerts):
    print(' '.join(a))
while True:
    gotAlerts = obtainLastAlerts()
    newAlerts = masto.filter_new_alerts_by_toots(gotAlerts, knownAlerts)
    if len(newAlerts) > 0:
        print(datetime.now())
        for a in newAlerts:
            masto.post_alert(a)
            knownAlerts.append(a)
    time.sleep(1)

