import requests
from urllib.parse import quote


class TG:
    def __init__(self, api_key, chat_id):
        self.api_key = api_key
        self.chat_id = chat_id

    def notify(self, message):
        message = quote(message)
        resp = requests.get(f'https://api.telegram.org/bot{self.api_key}/sendMessage?chat_id={self.chat_id}&text={message}&parse_mode=markdown&disable_web_page_preview=True')
        # print(resp.text)