import os
import json
import hashlib
from datetime import datetime as dt
from datetime import timedelta
from time import sleep

from dotenv import load_dotenv
import requests
import pyodbc
from db.db import SessionLocal
from db.models import YandexDirect

from logger.telegram import send_message

load_dotenv()


class YandexDirectConn:
    url = 'https://api.direct.yandex.com/json/v5/reports'
    __token = os.getenv('DIRECT_TOKEN')
    __clientLogin = os.getenv('clientLogin')

    headers = {
        "Authorization": "Bearer " + __token,
        "Client-Login": __clientLogin,
        "Accept-Language": "ru",
        "processingMode": "auto",
        "returnMoneyInMicros": "false",
        "skipReportHeader": "true",
        "skipColumnHeader": "true",
        "skipReportSummary": "true"
    }

    @staticmethod
    def get_date() -> str:
        date = (dt.now() - timedelta(1)).strftime("%Y-%m-%d")
        send_message(f'yandex_direct.get_date return {date}')
        return date

    def get_data(self, date=None) -> str:
        send_message(f'yandex_direct.get_data start with {date}')
        if date is None:
            date = self.get_date()
        body = {
            "method": "get",
            "params": {
                "SelectionCriteria": {
                    "DateFrom": date,
                    "DateTo": date
                },

                "FieldNames": [
                    "Date",
                    "CampaignName",
                    "Impressions",
                    "Clicks",
                    "Cost"
                ],
                "ReportName": f"r{date}",
                "Page": {
                    "Limit": 4000000
                },
                "ReportType": "CUSTOM_REPORT",
                "DateRangeType": "CUSTOM_DATE",
                "Format": "TSV",
                "IncludeVAT": "YES",
                "IncludeDiscount": "NO"
            }
        }
        body = json.dumps(body, indent=4)
        response = requests.post(self.url, body, headers=self.headers)
        print(response)
        return response

    @staticmethod
    def create_item(data: list) -> None:
        db = SessionLocal()
        for row in data:
            h_l = hashlib.md5(str(row).encode()).hexdigest()
            row.append(h_l)
            item = YandexDirect(*row)
            try:
                db.add(item)
                db.commit()
                db.refresh(item)
            except pyodbc.Error:
                print('double')
                pass

        send_message('yandex_direct item creating done')

    def run(self, date=None):
        data = []

        self.get_data(date)
        sleep(120)
        result = self.get_data(date).text.split()

        i = 0
        while i < len(result):
            k = i + 5
            item = result[i: k]
            data.append(item)
            i += 5
        print(data)
        self.create_item(data)



