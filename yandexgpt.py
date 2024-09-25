import requests
import json
from config import API_KEY
#обращение к yandexGPT 3 pro в синхронном режиме gpt://b1gpa0vaqbddbj9rqcpu/yandexgpt/latest
#yandexGPT lite 3 gpt://b1gpa0vaqbddbj9rqcpu/yandexgpt-lite/latest

def getYandexGPTResponse(systemRole, textPrompt, temperature):
    prompt = {
        "modelUri": "gpt://b1gpa0vaqbddbj9rqcpu/yandexgpt/latest",
        "completionOptions" : {
            "stream": False,
            #Температура влияет на вариативность сгенерированного текста: чем выше значение, тем более непредсказуемым будет результат выполнения запроса.
            #Укажите любое значение от 0 до 1, чтобы задать «креативность» модели.
            "temperature": f"{temperature}",             
            "maxTokens": "2000"
        },

        "messages": [
            {
                "role": "system",
                "text": f"{systemRole}"
            },
            {
                "role": "user",
                "text": f"{textPrompt}"
            }
        ]
    }
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {API_KEY}"
    }
    response = requests.post(url, headers=headers, json=prompt)
    #result = response.text
    #print(result)

    response_dict = json.loads(response.text)
    response_result0 = ((((response_dict['result'])['alternatives'])[0])['message'])['text']
    return response_result0

#"Напиши sql-запрос к таблице solutions, имеющей поля id (serial), description (text), cvss(float). Запрос должен отобрать выборку уязвимостей с cvss больше 8.5 и отсортировать по убыванию величины cvss"
            