import requests
import os
from xml.dom import minidom

class UpworkRssFeed:
    def __init__(self, url, db_path):
        self.url = url
        self.db_path = db_path

    def get_new_jobs(self):
        jobs = self.parse_feed()
        new_jobs = []
        parsed_jobs = self._get_parsed_jobs()
        for job in jobs[::-1]:
            if job['link'] not in parsed_jobs:
                new_jobs.append(job)
                parsed_jobs.append(job['link'])
        self._write_parsed_jobs(parsed_jobs)
        return new_jobs



    def parse_feed(self):
        jobs = []
        resp = requests.get(self.url)
        raw_xml = resp.text
        xmldoc = minidom.parseString(raw_xml)
        itemlist = xmldoc.getElementsByTagName('item')
        for item in itemlist:
            description = item.getElementsByTagName('description')[0].firstChild.nodeValue
            budget = self._extract_budget(description)            
            job = {
                'title': item.getElementsByTagName('title')[0].firstChild.nodeValue,
                'link': item.getElementsByTagName('link')[0].firstChild.nodeValue,
                'budget': budget
            }            
            jobs.append(job)
        return jobs

    def _extract_budget(self, description):
        budget = {'hourly': None, 'fixed': None}
        hr = '<b>Hourly Range</b>:'
        fr = '<b>Budget</b>:'
        if hr in description:
            budget['hourly'] = description.split(hr)[-1].split('<br />')[0].strip()
        if fr in description:
            budget['fixed'] = description.split(fr)[-1].split('<br />')[0].strip()
        return budget
    
    def _get_parsed_jobs(self):
        if not os.path.exists(self.db_path):
            return []
        with open(self.db_path) as file:
            job_links = file.readlines()
        return [link.strip() for link in job_links]

    def _write_parsed_jobs(self, job_links):
        with open(self.db_path, 'w') as file:
            file.write('\n'.join(job_links[-1000:]))
        