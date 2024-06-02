from django.contrib import admin
from .models import Stock, PriceRecord, Prediction

admin.site.register(Stock)
admin.site.register(PriceRecord)
admin.site.register(Prediction)
