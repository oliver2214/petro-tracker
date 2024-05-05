from django.shortcuts import redirect, render
from .influxdb.database import data_market, data_security
from datetime import datetime, timedelta
import json


# проинициализировал пока здесь, потом когда подыму базу данных уберу
TICKERS = ["BANE", "BANEP", "VJGZ", "VJGZP", "GAZP", "RTGZ", "RTGZ", "EUTR", "LKOH", "MFGS", "MFGSP",
           "NVTK", "CHGZ", "ROSN", "RNFT", "KRKN", "KRKNP", "JNOSP", "JNOS", "SNGS", "SNGSP", "TATN",
           "TATNP", "TRNFP", "YAKG"]


def index(request):
    data = {"stylesheet_file": "index.css",
            "exchanges": ["MOEX", "MOEX"]
            }
    return render(request, "tracker/index.html", data)


def auth(request):
    return render(request, "tracker/auth.html")


def market(request, exchange):
    # Для отображения информации о торгах нужна конкретная дата
    # Дату выбирает либо пользователь на странице, либо автоматически выбирается предыдущий день
    date_str = request.GET.get("date", None)
    if date_str:
        # Преобразование условного "2000-01-01" в datetime(2000, 1, 1)
        date = datetime(*[int(el) for el in date_str.split("-")])
    else:
        date = datetime.now() - timedelta(days=1)

    data = {
        "stylesheet_file": "base.css",
        "exchange": exchange,
        "data_table": data_market(date),
        "date": date,
        "todays_date": datetime.now().strftime('%Y-%m-%d')
    }

    return render(request, "tracker/market.html", data)


def security(request, exchange, ticker):
    # функцией data_security подтягиваются данные из influxdb по конкретному ticker
    if ticker not in TICKERS:
        return redirect(to="market")
    security_dynamics = data_security(exchange, ticker)
    data = {
        "stylesheet_file": "base.css",
        "ticker": ticker,
        'prices_json': json.dumps(security_dynamics),
    }

    return render(request, "tracker/security.html", data)
