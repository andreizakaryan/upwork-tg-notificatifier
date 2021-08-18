import json
import time

from UpworkRssFeed import UpworkRssFeed
from TG import TG


with open('config.json') as file:
    config = json.load(file)

tg = TG(config['api_key'], config['chat_id'])
parser = UpworkRssFeed(config['rss_url'], config['db_path'])

while True:
    try:
        jobs = parser.get_new_jobs()
        print(len(jobs))
        messages = []
        for job in jobs:
            budget = ''
            if job['budget']['fixed']:
                budget = f"*Fixed*: {job['budget']['fixed']}"
            if job['budget']['hourly']:
                budget = f"*Hourly Rate*: {job['budget']['hourly']}"
            messages.append(f"[New Job:]({job['link']})\n_{job['title']}_\n{budget}")
        for message in messages:
            tg.notify(message)
        pass
    except:
        pass
    time.sleep(60)
