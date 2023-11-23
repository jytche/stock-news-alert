import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

account_sid = "ACC_ID"
auth_token = "AUTH_TOKEN"

stock_api_key = "ENTER API KEY"
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "outputsize": "compact",
    "apikey": stock_api_key
}

news_api_key = "ENTER API KEY"
news_parameters = {
    "apiKey": news_api_key,
    "qInTitle": COMPANY_NAME,
    "language": "en"
}

response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
stock_prices = response.json()['Time Series (Daily)']
stock_prices_list = [value for (key, value) in stock_prices.items()]
yesterday_close = float(stock_prices_list[0]["4. close"])
day_before_close = float(stock_prices_list[1]["4. close"])

price_diff = yesterday_close - day_before_close
up_down = None
if price_diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

price_diff_pct = round(price_diff / yesterday_close * 100)


if abs(price_diff_pct) > 0.5:
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_data = news_response.json()

    news_data_slice = news_data["articles"][:3]
    print(news_data_slice)

    news_list = [f"{STOCK_NAME}: {up_down}{price_diff_pct}% \nHeadline: {article['title']}.\nBrief: "
                 f"{article['description']}" for article in news_data_slice]

    client = Client(account_sid, auth_token)
    for article in news_list:
        message = client.messages.create(
            body=article,
            from_='+TWILIO NUMBER',
            to='+ADDRESS NUMBER'
        )


