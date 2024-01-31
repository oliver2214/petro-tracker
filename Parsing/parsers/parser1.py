import requests
import re
from datetime import datetime


def parse_data(measurement):
    year = 2024
    month = 1
    for day in range(8, 9):
        date = f"{year}-{month}-{day}"

        SECIDS = ["BANE", "BANEP", "VJGZ", "VJGZP", "GAZP", "RTGZ", "RTGZ", "EUTR", "LKOH", "MFGS", "MFGSP", "NVTK", "CHGZ", "ROSN", "RNFT", "KRKN", "KRKNP", "JNOSP", "JNOS", "SNGS", "SNGSP", "TATN", "TATNP", "TRNFP", "YAKG"]

        text = ""
        for start in range(0, 300, 100):  # отображение нужной информации осуществляется по 100 элементов на страницу, поэтому приходится циклом по 100 считывать по частям
            url = f"https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/tqbr/securities.xml?date={date}&start={start}"  # определяем url откуда будем парсить данные
            text = text + requests.get(url).text  # получаем всю выборку

        data = []

        for i, line in enumerate(text.split("\n")):  # Пройдемся по всем строкам текста взятого с биржи для оптимизации, вместо поиска каждой необходимой акции
            info = re.findall(r'SHORTNAME="(.+?)".+SECID="(.+?)".+VALUE="(.+?)".+OPEN="(.+?)".+LOW="(.+?)".+HIGH="(.+?)".+WAPRICE="(.+?)".+CLOSE="(.+?)"', line)  # тут происходит вычленение нужной информации со строки: цена, название и прочее
            if info and info[0][1] in SECIDS:
                timestamp = int(datetime(year, month, day).timestamp() * 1e9)
                shortname = info[0][0].replace(" ", "\ ")
                line = f'{measurement},SECID={info[0][1]},SHORTNAME="{shortname}" VALUE={info[0][2]},OPEN={info[0][3]},LOW={info[0][4]},HIGH={info[0][5]},WAPRICE={info[0][6]},CLOSE={info[0][7]} {timestamp}'
                data.append(line)

        return data


if __name__ == "__main__":  # убрать
    print(parse_data("a"))
