import datetime
import json
import time

import requests

TEMPLATE = """
<p style="font-weight: bold; font-size: 4em;">{days}</p>
<br/>
<p>This post automatically updates. All changes will be overridden.</p>
"""

with open('config.json', 'r') as f:
    config = json.load(f)

def saveConfig():
    global config
    assert config
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)

def loadDictFromJson():
    result = {}
    for element in config['cookies']:
        result[element['name']] = element['value']
    return result

session = requests.Session()
requests.utils.add_dict_to_cookiejar(
    session.cookies,
    loadDictFromJson()
)

def updatePost():
    print("Update", datetime.datetime.now())
    payload = {
        "method": "content.update",
        "params": {
            "cid": "jnj3uc5rdipis",
            "subject": "Days Since Last Project Issue",
            "content": TEMPLATE.format(
                days=(datetime.date.today() - datetime.date(2018, 10, 25)).days
            ),
            "anonymous": "no",
            "type": "note",
            "folders": ["project1", "project2", "project3", "project4", "project5"],
            "revision": config['revisionCount']
        }
    }

    params = {
        "method": "content.update",
    }

    res = session.post(
        "https://piazza.com/logic/api",
        params=params,
        json=payload,
        headers={
            "CSRF-Token": config['csrf-token']
        }
    )

    config['revisionCount'] += 1
    saveConfig()

    if not res.json()['result']:
        print(res.json())


def main():
    updatePost()
    while True:
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        midnight = datetime.datetime(year=tomorrow.year, month=tomorrow.month, 
                        day=tomorrow.day, hour=0, minute=0, second=0)
        secondsTillMidnight = (midnight - datetime.datetime.now()).seconds
        time.sleep(secondsTillMidnight)

        updatePost()



if __name__ == '__main__':
    main()
