import json
from datetime import datetime

from django.shortcuts import redirect, render

from .services import get_date
from .influxdb.database import get_data_market, get_data_security
from .models import Exchanges, Securities


def index(request):
    # Получаем все объекты из модели Exchanges и извлекаем значения exchange_code
    exchanges = Exchanges.objects.values_list('exchange_code', flat=True)

    # Преобразуем QuerySet в список
    exchanges_list = list(exchanges)

    data = {"stylesheet_file": "index.css",
            "exchanges": exchanges_list
            }
    return render(request, "tracker/index.html", data)


def auth(request):
    return render(request, "tracker/auth.html")


def market(request):
    # Для отображения информации о торгах нужна конкретная дата
    # Дату выбирает либо пользователь на странице, либо автоматически выбирается предыдущий день
    date = get_date(request.GET.get("date", None))

    # Получаем все объекты из модели Exchanges и извлекаем значения exchange_code
    exchanges_responce_orm = Exchanges.objects.values_list('exchange_code', 'currency', 'shortname')

    # Преобразуем QuerySet в словарь бирж
    exchanges = {exchange[0]: {"currency": exchange[1], "exchange_shortname": exchange[2]} for exchange in list(exchanges_responce_orm)}

    # Слияние данных influxdb и postgresql, чтобы консистентно отправить в html
    for exchange_code in exchanges.keys():
        exchanges[exchange_code]["stocks"] = get_data_market(date, exchange=exchange_code)
        if exchanges[exchange_code]["stocks"]:
            securities = Securities.objects.filter(exchange__exchange_code=exchange_code).values('ticker', 'shortname')
            for security in securities:
                if exchanges[exchange_code]["stocks"].get(security['ticker'], False):
                    exchanges[exchange_code]["stocks"][security['ticker']]['SHORTNAME'] = security['shortname']

    # Если все разы из БД вернулось False, то exchanges = False (Отсутствует подключение к БД)
    if all(map(lambda exchange: exchange["stocks"] is False, exchanges.values())):
        is_db_connected = False
    else:
        is_db_connected = True

    if all(map(lambda exchange: len(exchange["stocks"]) == 0, exchanges.values())):
        no_data_in_db = True
    else:
        no_data_in_db = False

    data = {
        "stylesheet_file": "base.css",
        "data_table": exchanges,
        "date": date,
        "todays_date": datetime.now().strftime('%Y-%m-%d'),
        "is_db_connected": is_db_connected,
        "no_data_in_db": no_data_in_db,
    }

    return render(request, "tracker/market.html", data)


def security(request, exchange_code, ticker):
    try:
        # Проверяем, существует ли указанная акция в указанной бирже
        exchange = Exchanges.objects.get(exchange_code=exchange_code.upper())
        security = Securities.objects.get(exchange=exchange, ticker=ticker.upper())
    except (Exchanges.DoesNotExist, Securities.DoesNotExist):
        # Если акция или биржа не существует, делаем редирект на страницу рынка
        return redirect(to="market")

    # Получаем данные о динамике цены акции из функции data_security
    security_dynamics = get_data_security(exchange_code, ticker)
    if security_dynamics is False:
        # Если данные о динамике цены акции недоступны, делаем редирект на страницу рынка
        return redirect(to="market")

    security_data = {
        "ticker": security.ticker,
        "shortname": security.shortname,
        "description": security.description,
        "site": security.site,
        "CEO": security.CEO,
        "ISIN": security.ISIN,
        "currency": exchange.currency,
        "exchange_code": exchange_code,
    }

    data = {
        "stylesheet_file": "base.css",
        'prices_json': json.dumps(security_dynamics),
        'security_data': security_data,
    }

    return render(request, "tracker/security.html", data)


def exchange(request, exchange_code):
    try:
        # Проверяем, существует ли указанная биржа
        exchange = Exchanges.objects.get(exchange_code=exchange_code.upper())
    except Exchanges.DoesNotExist:
        return redirect(to="market")

    date = get_date(request.GET.get("date", None))

    # Получаем данные о ценных бумагах для данной биржи
    securities = get_data_market(date, exchange=exchange_code)

    # Получаем данные о ценных бумагах из базы данных
    securities_orm = Securities.objects.filter(exchange__exchange_code=exchange_code).values('ticker', 'shortname')

    # Обновляем данные о ценных бумагах в словаре
    for security in securities_orm:
        if securities.get(security['ticker'], False):
            securities[security['ticker']]['SHORTNAME'] = security['shortname']

    exchange_data = {
        "exchange_code": exchange_code,
        "shortname": exchange.shortname,
        "description": exchange.description,
        "country": exchange.country,
        "currency": exchange.currency,
        "site": exchange.site,
    }

    data = {
        "stylesheet_file": "base.css",
        "exchange": exchange_data,
        "securities": securities,
        "date": date,
        "todays_date": datetime.now().strftime('%Y-%m-%d')
    }
    return render(request=request, template_name="tracker/exchange.html", context=data)
