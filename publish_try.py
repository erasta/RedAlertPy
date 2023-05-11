from mastodon import Mastodon
import json

secrets = json.load(open("secrets.json"))
# print(secrets)
# exit()

# Initialise Mastodon API
mastodon = Mastodon(
    client_id = secrets["client_id"],
    client_secret = secrets["client_secret"],
    access_token = secrets["access_token"],
    api_base_url = 'https://' + secrets["mastodon_hostname"],
)
toot_text = 'now unlisted'
mastodon.status_post(toot_text, in_reply_to_id=None, visibility='unlisted') #, media_ids=[media_dict] )
