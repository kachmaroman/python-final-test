import time
import random
import requests
import openai
from key import key
openai.api_key = key

def get_time(text):
    current_time = time.localtime()
    output_time = f'{current_time.tm_hour}:{current_time.tm_min}'

    return  {"час": output_time}

def get_random_number(text):
    random_number = random.randint(1, 100)

    return {"число": str(random_number)}

def get_usd_currency(text):
    result = requests.get("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")
    result = result.json()
    total = str(round(float(result[1]['sale']), 2))
    total = total.split('.')

    return {"курс_грн": total[0], "курс_копійка": total[1]}