from django.urls import path
from tracker import views

urlpatterns = [
    path("", views.index, name="index"),
    path("auth/", views.auth, name="auth"),
    path("market/<slug:exchange>/", views.market, name="market"),
    path("security/<slug:exchange>/<slug:ticker>/", views.security, name="security"),
]
