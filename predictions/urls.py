from django.urls import path
from .views import select_stock, display_indicators

urlpatterns = [
    path('select-stock/', select_stock, name='select-stock'),
    path('results/', display_indicators, name='display_indicators')
]
