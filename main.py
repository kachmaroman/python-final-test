from http.client import responses
from logging import fatal

import speech_recognition as sr
import json
import openai
from key import key
openai.api_key = key

from output import say
from functions import *

def load_speech():
    with open("speech.json", "r", encoding='utf-8') as f:
        data = json.load(f)
    return data

data = load_speech()

def speech_commands(text):
    result = False

    for phrase in data:
        for input_words in phrase['input']:
            if input_words in text.lower():
                result = True
                output = random.choice(phrase["output"])
                function_name = phrase.get("function")

                if function_name:
                    func = globals().get(function_name)

                    if func:
                        output_func = func(text)

                        for key in output_func.keys():
                            output = output.replace(f'[{key}]', output_func[key])

                say(output)

    return result

def main():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        say("Привіт, я твій голосовий помічник, чим можу допомогти?")

        while True:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            try:
                text = recognizer.recognize_google(audio, language='uk-UA')
                result = speech_commands(text)

                if result == False:
                    prompt = f'''Ти маєш генерувати короткі відповіді для голосового помічника, без зайвого тексту.
                            Надаю те що запитує користувач: {text}'''

                    response = openai.ChatCompletion().create(
                        model="gpt-4o-mini",
                        messages = [
                            {"role": "user", "content": prompt}
                        ]
                    )

                    say(response["choices"][0]["message"]["content"].strip())

            except sr.UnknownValueError:
                say("Вибачте, я вас не розумію. Повторіть, будь ласка")
            except sr.RequestError as e:
                print("Request error")
            except sr.WaitTimeoutError:
                print("Wait timeout")
            except (openai.error.RateLimitError, openai.error.AuthenticationError):
                say("Вибачте, не зможу відповісти")

main()