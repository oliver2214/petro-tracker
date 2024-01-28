from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render


def index(request):
    response = render_to_string("tracker/index.html")
    return HttpResponse(response)


def auth(request):
    return render(request, "tracker/auth.html")


def market(request):
    data = {
        "data_table": [{
            'id': 1,
            'symbol': 'ABC',
            'company_name': 'Company A',
            'last_price': 100.00,
            'price_change': +2.5,
            'first_price': 98.00,
            'min_price': 95.00,
            'max_price': 96.50,
            'volume': 1000000,
            'last_update': '12:30',
        }, {
            'id': 2,
            'symbol': 'XYZ',
            'company_name': 'Company X',
            'last_price': 50.50,
            'price_change': -1.2,
            'first_price': 51.00,
            'min_price': 49.80,
            'max_price': 50.20,
            'volume': 500000,
            'last_update': '13:45',
        }, {
            'id': 3,
            'symbol': 'DEF',
            'company_name': 'Company D',
            'last_price': 75.25,
            'price_change': +0.8,
            'first_price': 74.50,
            'min_price': 73.80,
            'max_price': 75.00,
            'volume': 750000,
            'last_update': '16:15',
        },
        ]
    }

    return render(request, "tracker/market.html", data)
