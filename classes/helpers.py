def select_closing_prices(df):
    closing_prices = df['Close'].to_list()
    return closing_prices

def get_price_history(ticker, start_date, end_date):
    price_history = ticker.history(start=start_date, end=end_date)
    return price_history
