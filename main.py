# -*- coding: utf-8 -*-
# !/usr/bin/env python3

import schedule
import time
import csv
import pandas as pd
import os
import logging
from requests_html import HTMLSession
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import sqlalchemy as sa

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.WARNING)
city = input('Get weather for town: ')


def job():
    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    s = HTMLSession()
    url = f'https://www.google.com/search?q=weather+{city}'

    r = s.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                          'like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.72'})

    temp = r.html.find('span#wob_tm', first=True).text
    unit = r.html.find('div.vk_bk.wob-unit span.wob_t', first=True).text
    span = r.html.find('div.VQF4g', first=True).find('span#wob_dc', first=True).text
    town = r.html.find('div.VQF4g', first=True).find('div#wob_loc', first=True).text
    other = r.html.find('div.wtsRwe', first=True).text

    df = [city, temp, unit, span, other]
    res = [item.replace('\n', ' ') for item in df]
    print(res)

    if os.path.isfile('pogoda.csv'):
        pass
    else:
        with open('pogoda.csv', 'w', newline='') as create_file_header:
            writer = csv.writer(create_file_header, delimiter=';')
            writer.writerow(["Miasto", "Stopnie", "Jednostka", "Zachmurzenie", "Inne"])

    with open('pogoda.csv', 'a', newline='', encoding="utf8") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(res)


# def RRCSV():
#     alchemyEngine = create_engine('postgresql+psycopg2://bartegu:encore221@localhost/postgres')
#     meta = MetaData()
#     check_tbl = sa.inspect(alchemyEngine)
#     if check_tbl.has_table("etl_pogoda", schema="public"):
#         pass
#     else:
#         etl_pogoda = Table(
#             'etl_pogoda', meta,
#             Column("Miasto", String),
#             Column("Stopnie", Integer),
#             Column("Jednostka", String),
#             Column("Zachmurzenie", String),
#             Column("Inne", String)
#         )
#     meta.create_all(alchemyEngine)


while True:
    schedule.run_pending()
    time.sleep(5)
    schedule.every(10).seconds.do(job)
#    schedule.every(10).seconds.do(RRCSV)
# schedule.every(5).seconds.do(openCSV)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)
