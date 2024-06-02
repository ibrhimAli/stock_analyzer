import os
from django.shortcuts import render, redirect
from .forms import StockSelectionForm
from .utils.get_historical_data import get_historical_data_url
from .utils.stock_symbols import stock_dict
from .indicators.run_indicators import indicators_result

def select_stock(request):
    
    if request.method == 'POST':
        form = StockSelectionForm(request.POST, stock_dict=stock_dict)
        if form.is_valid():
            selected_stock = form.cleaned_data['stock']
            time_frame = form.cleaned_data['timeframe']
            file_path = get_historical_data_url(selected_stock)
            print(f"==========================Analyzing {selected_stock} stock in {time_frame} time frame===================================")
            if os.path.exists(file_path):
            # Proceed to analyze the data in file_path
                context = indicators_result(file_path, time_frame, selected_stock)
                #request.session['df_html'] = df.to_html()
                return render(request, 'predictions/display_indicators.html', context)
                
            else:
            # Handle error: file not downloaded or URL not found
                pass
    else:
        form = StockSelectionForm(stock_dict=stock_dict)
    return render(request, 'predictions/select_stock.html', {'form': form})


def display_indicators(request, context):
    df_html = request.session.get('df_html', None)
    if df_html:
        return render(request, 'predictions/display_indicators.html', context)
    else:
        return render(request, 'predictions/error.html', {'message': 'No data available.'})