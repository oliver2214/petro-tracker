from django.urls import path
from tracker import views

urlpatterns = [
    path("", views.index, name="index"),
    path("market/", views.market, name="market"),
    path("exchange/<slug:exchange_code>/", views.exchange, name="exchange"),
    path("security/<slug:exchange_code>/<slug:ticker>/", views.security, name="security"),
]
