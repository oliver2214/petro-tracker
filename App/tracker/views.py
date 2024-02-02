from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from .influxdb.database import data_market
from datetime import datetime, timedelta


def index(request):
    response = render_to_string("tracker/index.html")
    return HttpResponse(response)


def auth(request):
    return render(request, "tracker/auth.html")


def market(request):
    # Для отображения информации о торгах нужна конкретная дата
    # Дату выбирает либо пользователь на странице, либо автоматически выбирается предыдущий день
    date_str = request.GET.get("date", None)
    if date_str:
        # Преобразование "2000-01-01" в datetime(2000, 1, 1)
        date = datetime(*[int(el) for el in date_str.split("-")])
    else:
        date = datetime.now() - timedelta(days=1)

    data = {
        "data_table": data_market(date),
        "date": date,
        "todays_date": datetime.now().strftime('%Y-%m-%d')
    }

    return render(request, "tracker/market.html", data)


def security(request, secid):
    data = {
        "secid": secid,
    }

    return render(request, "tracker/security.html", data)
