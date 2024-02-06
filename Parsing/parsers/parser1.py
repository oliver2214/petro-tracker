import requests
import re
from datetime import datetime, timedelta


def parse_data_once_a_day(measurement, date_from: datetime, date_to: datetime):
    data = []

    while date_to >= date_from:
        date = f"{date_from.year}-{date_from.month}-{date_from.day}"

        SECIDS = ["BANE", "BANEP", "VJGZ", "VJGZP", "GAZP", "RTGZ", "RTGZ", "EUTR", "LKOH", "MFGS", "MFGSP",
                  "NVTK", "CHGZ", "ROSN", "RNFT", "KRKN", "KRKNP", "JNOSP", "JNOS", "SNGS", "SNGSP", "TATN",
                  "TATNP", "TRNFP", "YAKG"]

        text = ""

        # отображение нужной информации осуществляется по 100 элементов на страницу,
        # поэтому приходится циклом по 100 считывать по частям
        start = 0
        total = 1
        while total > start:
            # определяем url откуда будем парсить данные
            url = f"https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/tqbr/securities.xml?date={date}&start={start}"  # noqa

            text = text + requests.get(url).text  # получаем всю выборку
            # переменная total - количество акций на всех страницах
            if total == 1:
                total = re.findall(r'TOTAL="(\d+)"', text)
                if total:
                    total = int(total[0])
            start += 100

        for line in text.split("\n"):  # Пройдемся по всем строкам текста
            # взятого с биржи для оптимизации, вместо поиска каждой необходимой акции

            # тут происходит вычленение нужной информации со строки: цена, название и пр при помощи регулярных выражений
            info = re.findall(r'SHORTNAME="(.+?)".+SECID="(.+?)".+VALUE="(.+?)".+OPEN="(.+?)".+LOW="(.+?)".+HIGH="(.+?)".+WAPRICE="(.+?)".+CLOSE="(.+?)"', line) # noqa

            # проходим по каждой строке с акциями, если она содержит акцию из SECIDS то работаем с ней
            if info and info[0][1] in SECIDS:
                timestamp = int((datetime(date_from.year, date_from.month, date_from.day, 20, 50) + timedelta(hours=3)).timestamp() * 1e9) # noqa
                # для influxdb пришлось добавить "\ ", т.к. запросы для influx содержат служебные пробелы
                shortname = info[0][0].replace(" ", "\ ")
                # Формируем строку-запрос для бд на запись, то есть эта строка добавит лишь 1 "строку" в бд
                line = f'{measurement},SECID={info[0][1]},SHORTNAME="{shortname}" VALUE={info[0][2]},OPEN={info[0][3]},LOW={info[0][4]},HIGH={info[0][5]},WAPRICE={info[0][6]},CLOSE={info[0][7]} {timestamp}' # noqa
                # добавляем эту строку в общий запрос. В конечном итоге получаем один большой запрос на запись данных
                data.append(line)

        date_from += timedelta(days=1)
    # запрос может содержать данные за несколько дней и месяцев
    return data
