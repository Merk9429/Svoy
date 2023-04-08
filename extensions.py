import json
import requests
from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote, base, amount):
        try:
            quote_key = keys[quote.lower()]
        except KeyError:
            return APIException(f"Валюта {quote} не найдена!")

        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        if quote_key == base_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={base_key}&from={quote_key}&amount={amount}"

        headers = {
            "apikey": "9eIUYXxL1xaVY0nVrvY0JI5UXTtTbtMY"
        }

        response = requests.request("GET", url, headers=headers)
        resp = json.loads(response.content)
        conclusion = resp['result']
        return round(conclusion)
