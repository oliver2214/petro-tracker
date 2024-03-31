from django.urls import path
from tracker import views

urlpatterns = [
    path("", views.index, name="index"),
    path("auth/", views.auth, name="auth"),
    path("market/", views.market, name="market"),
    path("security/<slug:secid>/", views.security, name="security"),
]
