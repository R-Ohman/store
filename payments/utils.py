import requests

from payments.models import Currency, ExchangeRate
from store.settings import BASE_CURRENCY


def update_exchange_rates():
    base_currency = Currency.objects.get(code=BASE_CURRENCY)
    target_currencies = Currency.objects.exclude(code=BASE_CURRENCY)

    for target_currency in target_currencies:
        # Выполните запрос к веб-сервису, предоставляющему курсы валют
        url = "https://api.exchangerate.host/latest"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            rates = data.get('rates')
            rate = rates[target_currency.code] / rates[base_currency.code]

            exchange_rate = ExchangeRate.objects.filter(base_currency=base_currency, target_currency=target_currency).first()
            exchange_rate.rate = rate
            exchange_rate.save()
