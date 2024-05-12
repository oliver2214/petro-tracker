import json
from datetime import datetime, timedelta

from django.shortcuts import redirect, render
from .influxdb.database import data_market, data_security
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
    date_str = request.GET.get("date", None)
    if date_str:
        # Преобразование условного "2000-01-01" в datetime(2000, 1, 1)
        date = datetime(*[int(el) for el in date_str.split("-")])
    else:
        # Если дата не указана, устанавливается по умолчанию предыдущий день
        date = datetime.now() - timedelta(days=1)

    # Получаем все объекты из модели Exchanges и извлекаем значения exchange_code
    exchanges_responce_orm = Exchanges.objects.values_list('exchange_code', flat=True)

    # Преобразуем QuerySet в словарь бирж
    exchanges = {exchange: None for exchange in list(exchanges_responce_orm)}

    for exchange in exchanges.keys():
        exchanges[exchange] = data_market(date, exchange=exchange)
        if exchanges[exchange]:
            securities = Securities.objects.filter(exchange__exchange_code=exchange).values('ticker', 'shortname')
            for security in securities:
                exchanges[exchange][security['ticker']]['SHORTNAME'] = security['shortname']

    # Если все разы из БД вернулось False, то exchanges = False (Отсутствует подключение к БД)
    if all(map(lambda exchange: exchange is False, exchanges.values())):
        exchanges = False

    if all(map(lambda exchange: len(exchange) == 0, exchanges.values())):
        exchanges = []

    data = {
        "stylesheet_file": "base.css",
        "data_table": exchanges,
        "date": date,
        "todays_date": datetime.now().strftime('%Y-%m-%d')
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
    security_dynamics = data_security(exchange_code, ticker)
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
        "exchange_code": exchange_code,
    }

    # Формируем контекст для передачи данных в шаблон
    data = {
        "stylesheet_file": "base.css",
        "ticker": ticker,
        'prices_json': json.dumps(security_dynamics),
        'security_data': security_data,
    }

    return render(request, "tracker/security.html", data)
