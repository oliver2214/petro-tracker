from django.urls import path
from tracker import views

urlpatterns = [
    path("", views.index, name="home"),
    path("auth/", views.auth, name="auth"),
    path("market/", views.market, name="market"),
]
