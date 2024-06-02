import pandas as pd

def load_data(file_path):
    # Define the column names in the order they are present in the CSV
    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    # Load the CSV file with no header (header=None) and assign the column names
    df = pd.read_csv(file_path, header=None, names=columns)
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.drop_duplicates(subset='Date')
    # Set 'Date' as the DataFrame index
    df.set_index('Date', inplace=True)
    return df