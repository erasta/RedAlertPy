# RedAlertPy
Red alert (Tzeva Adom) for publishing updates of rocket attacks on Israel

Python program that tracks Pikud HaOref updates of rocket attacks on Israel.
New updates are then published to Mastodon network on https://kishkush.net/@redAlert

Note: this updates are not to be used as realtime emergency data, as latency and bugs could cause delays.

### Deploy
```sh
git clone https://github.com/erasta/RedAlertPy.git
cd RedAlertPy
pipenv shell && pipenv install
```
- Create a mastodon bot user (don't forget to mark it as a bot on settings > profile > This is a bot account)  
- Create an application for that bot (on settings > applications > new application)  
- Copy the file `secrets.example.json` to `secrets.json` and fill the details from the application you just created  

### Run
```sh
pipenv run python -m RedAlert --posts --errors-to @<myuser>@host.name &
```

Output would be stored on `last_run.txt`  
Polygon cache would be on `cache.geojson`
