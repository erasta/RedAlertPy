import time
from datetime import datetime
from mastodon import Mastodon
import json

from AlertFetch import *
from MastoAlerts import MastoAlerts

masto = MastoAlerts()
while True:
    gotAlerts = obtainLastAlerts()
    newAlerts = masto.filter_new_alerts_by_toots(gotAlerts)
    if len(newAlerts) > 0:
        print(datetime.now())
        for a in newAlerts:
            masto.post_alert(a)
    time.sleep(1)

