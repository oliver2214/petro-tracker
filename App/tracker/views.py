from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from .influxdb.database import data_market


def index(request):
    response = render_to_string("tracker/index.html")
    return HttpResponse(response)


def auth(request):
    return render(request, "tracker/auth.html")


def market(request):
    data = {
        "data_table": data_market()
    }

    return render(request, "tracker/market.html", data)


def security(request, secid):
    data = {
        "secid": secid,
    }

    return render(request, "tracker/security.html", data)
