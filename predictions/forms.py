from django import forms

class StockSelectionForm(forms.Form):
    stock = forms.ChoiceField(choices=[], label="Select a Stock", widget=forms.Select(attrs={'class': 'form-control'}))
    timeframe = forms.ChoiceField(
        choices=[
            ('short', 'Short Term (1-3 months)'),
            ('medium', 'Medium Term (3-6 months)'),
            ('long', 'Long Term (1 year)')
        ],
        label="Select Timeframe",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        stock_dict = kwargs.pop('stock_dict', {})  # Remove 'stock_dict' from kwargs before calling super
        super(StockSelectionForm, self).__init__(*args, **kwargs)  # Now call super without the extra kwarg
        self.fields['stock'].choices = [(key, f"{key} - {value}") for key, value in stock_dict.items()]
