import requests
import json
from yandexgpt import getYandexGPTResponse


class CVE:
    def __init__(self):
        self.name = ""
        self.description = ""        
        self.reference = ""
        self.cvss = 0.0
        self.solution = ""
    def __init__(self, name, description, references, cvss):
        self.name = name
        self.description = description        
        self.reference = references
        self.cvss = cvss
        self.solution = ""
    
   
    def translateDescription(self):
        desc = self.description
        translation = getYandexGPTResponse("ты- профессиональный переводчик и специалист по информационной безопасности", f"переведи описание уязвимости с английского на русский, чтобы текст был понятен русскоговорящему человеку. Не пиши дополнительный текст, только перевод. Описание: {desc}", 0.3)
        self.description = translation

    def find_info(name):
        url = f"https://cveawg.mitre.org/api/cve/{name}"
        response = requests.get(url)
        if response.ok:             
            response_dict = json.loads(response.text)
            try:
                response_description = ((((response_dict["containers"])['cna'])['descriptions'])[0])['value']
                if 'references' in ((response_dict["containers"])['cna']):
                    response_references_arr = (((response_dict["containers"])['cna'])['references'])
                    response_references_str = ""
                    for i in response_references_arr:
                        response_references_str = f"{response_references_str}{i['url']}\n" 
                if 'metrics' in ((response_dict["containers"])['cna']):
                    response_cvss = (((((response_dict["containers"])['cna'])['metrics'])[0])['cvssV3_0'])['baseScore']
                    print(response_cvss)                
                else:
                    response_cvss = 0
                cve = CVE(name, response_description, response_references_str, response_cvss)
                cve.translateDescription()
                return cve
            except Exception as _ex:
                print('[INFO] Error in json parsing', _ex)
        else:
            return 0  
  

    