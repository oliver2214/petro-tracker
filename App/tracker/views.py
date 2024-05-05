from django.shortcuts import redirect, render
from .influxdb.database import data_market, data_security
from datetime import datetime, timedelta
import json


# проинициализировал пока здесь, потом когда подыму базу данных уберу
exchanges = {
        "MOEX": ["BANE", "BANEP", "VJGZ", "VJGZP", "GAZP", "RTGZ", "RTGZ", "EUTR", "LKOH", "MFGS", "MFGSP",
                 "NVTK", "CHGZ", "ROSN", "RNFT", "KRKN", "KRKNP", "JNOSP", "JNOS", "SNGS", "SNGSP", "TATN",
                 "TATNP", "TRNFP", "YAKG"],
        "NASDAQ": ["ACDC", "APA", "ARLP", "BANL", "BRY", "CHK", "CHKEL", "CHKEW", "CHKEZ", "CHRD", "CLMT",
                   "DMLP", "DWSN", "EPSN", "FANG", "HPK", "HPKEW", "MARPS", "NEXT", "PAA", "PAGP", "PFIE",
                   "PNRG", "PRTG", "PTEN", "RCON", "USEG", "VNOM"],
        "SSE": ["601918", "600688", "601015", "600121", "600256", "600997", "601857", "600971", "601101",
                "605090", "600395", "600546", "601011", "600968", "600985", "600123", "600777", "601898",
                "601666", "600348", "600758", "601001", "601699", "601225", "600180", "601088", "600938",
                "600792", "900948", "600725", "600740", "600508", "603619", "600403", "600188"]
}


def index(request):
    data = {"stylesheet_file": "index.css",
            "exchanges": ["MOEX", "NASDAQ"]
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
        # Если дата не указана, устанавливается по умолчанию предыдущий день
        date = datetime.now() - timedelta(days=1)

    data = {
        "stylesheet_file": "base.css",
        "exchange": exchange,
        "data_table": data_market(date, exchange=exchange),
        "date": date,
        "todays_date": datetime.now().strftime('%Y-%m-%d')
    }

    return render(request, "tracker/market.html", data)


def security(request, exchange, ticker):
    # функцией data_security подтягиваются данные из influxdb по конкретному ticker
    if exchange.upper() not in exchanges or ticker.upper() not in exchanges[exchange.upper()]:
        return redirect(to="market", exchange=exchange)
    security_dynamics = data_security(exchange, ticker)
    if security_dynamics is False:
        return redirect(to="market", exchange=exchange)
    data = {
        "stylesheet_file": "base.css",
        "ticker": ticker,
        'prices_json': json.dumps(security_dynamics),
    }

    return render(request, "tracker/security.html", data)
