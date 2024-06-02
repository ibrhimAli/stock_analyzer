from django.db import models

class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'predictions'
        
    def __str__(self):
        return f"{self.symbol} - {self.name}"

class PriceRecord(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()

    def __str__(self):
        return f"{self.stock.symbol} - {self.date}"

class Prediction(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    prediction_date = models.DateField()
    predicted_close = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.stock.symbol} - Prediction for {self.prediction_date}"
