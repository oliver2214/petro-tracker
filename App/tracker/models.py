from django.db import models


class Exchanges(models.Model):
    exchange_code = models.CharField(max_length=16, unique=True)
    shortname = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=128, blank=True)
    currency = models.CharField(max_length=16)


class Securities(models.Model):
    ticker = models.CharField(max_length=32, db_index=True)
    shortname = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    site = models.CharField(max_length=64, blank=True)
    CEO = models.CharField(max_length=64, blank=True)
    ISIN = models.CharField(max_length=32)

    exchange = models.ForeignKey("Exchanges", on_delete=models.PROTECT)
