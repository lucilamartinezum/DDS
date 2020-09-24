from main import scheduler
import requests


@scheduler.task("interval", id="consume_earthquake", seconds=30)
def consume_service():
    query = requests.get(url='https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01'
                             '&endtime=2014-01-02', headers={"content-type":"application/json"})
    print(query.text)