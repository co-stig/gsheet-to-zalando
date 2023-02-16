#!/bin/env python3

import configparser
import csv
import io
import os
import os.path
import time

import requests
from apiclient import discovery
from google.oauth2 import service_account
from schedule import repeat, every, run_pending


def to_csv(data):
    s = io.StringIO()
    writer = csv.writer(s, delimiter=';', quotechar='"')
    writer.writerows(data)
    return s.getvalue()


class Zalando:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        settings = config['Settings']
        self.zalando_client_id = settings['ZalandoClientId']
        self.zalando_api_key = settings['ZalandoApiKey']

    def send(self, s, validate=True):
        res = requests.put(
            f"https://merchants-connector-importer.zalandoapis.com/{self.zalando_client_id}/{'validate' if validate else 'stock.csv'}",
            headers={
                'x-api-key': self.zalando_api_key,
                'content-type': "application/csv",
                'cache-control': "no-cache"
            },
            data=s
        )
        if res.status_code == 200:
            print('Update sent successfully')
        else:
            print('An issue while sending updates to Zalando:', res.json())


class Spreadsheet:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        settings = config['Settings']
        self.spreadsheet_id = settings['SpreadsheetId']
        self._initialize_google_client()

    def _initialize_google_client(self):
        self._google_client = discovery.build(
            'sheets',
            'v4',
            credentials=service_account.Credentials.from_service_account_file(
                os.path.join(os.getcwd(), 'client_secret.json'),
                scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
            )
        ).spreadsheets()

    def read_spreadsheet(self):
        return self._google_client.values().get(
            spreadsheetId=self.spreadsheet_id,
            range='Articles'
        ).execute().get('values', [])


@repeat(every().hour.at(':00'), Spreadsheet(), Zalando())
def update_stock(sheet, zalando):
    data = to_csv(sheet.read_spreadsheet())
    zalando.send(data, validate=False)


if __name__ == '__main__':
    while True:
        run_pending()
        time.sleep(1)
