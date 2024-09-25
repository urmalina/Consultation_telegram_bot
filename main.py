import telebot
from telebot import types
from config import ssh
from bd_queries import getSolution, getDescription, getReference, isExist, doQuery
from yandexgpt import getYandexGPTResponse
from cve_parser import CVE

bot = telebot.TeleBot(ssh, threaded= False)

#обработчики команд  
@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Привет! Напиши название уязвимости или воспользуйся командами в нижней панели')
   
    
@bot.message_handler(commands=['viewdescription'])
def main(message):
    bot.send_message(message.chat.id, 'Для просмотра описания уязвимости, напиши ее название. ')
    bot.register_next_step_handler(message, find_description)

def find_description(message):
    name = message.text
    ans = getDescription(name)
    if ans!=None:
        bot.send_message(message.chat.id, f"{ans}") 
    else:
        bot.send_message(message.chat.id, f'У меня нет информации по уязвимости "{name}". Проверьте правильность написания и попробуйте снова.')    


@bot.message_handler(commands=['findsolution'])
def main(message):
    bot.send_message(message.chat.id, 'Для просмотра информации по устранению уязвимости, напиши ее название. ')
    bot.register_next_step_handler(message, find_solution)
def find_solution(message):
    vuln = message.text
    ans = getSolution(vuln)
    if ans!=None:
        bot.send_message(message.chat.id, f"{ans}") 
    else:
        bot.send_message(message.chat.id, f'У меня нет информации по устранению уязвимости "{vuln}". Проверьте правильность написания и попробуйте снова.')    

@bot.message_handler(commands=['references'])
def main(message):
    bot.send_message(message.chat.id, 'Для просмотра ссылок, напиши название уязвимости. ')
    bot.register_next_step_handler(message, get_references)
def get_references(message):
    vuln = message.text
    ans = getReference(vuln)
    if ans!=None:
        bot.send_message(message.chat.id, f"{ans}") 
    else:
        bot.send_message(message.chat.id, f'У меня нет информации по уязвимости "{vuln}". Проверьте правильность написания и попробуйте снова.')    

# @bot.message_handler(commands=['stopgptmode'])
# def main(message):
#     bot.send_message(message.chat.id, 'Работа с AI ассистентом приостановлена')

@bot.message_handler(commands=['gptmode'])
def main(message):
    bot.send_message(message.chat.id, 'Сформулируйте запрос')
    bot.register_next_step_handler(message, get_response)
def get_response(message):
    if(message.text != "/stopgptmode"):
        ans0 = getYandexGPTResponse("опытный sql-разработчик", f"Напиши sql-запрос для получения выборки по таблице solutions с полями: id, name (text) - Название уязвимости (название обычно включает год обнаружения в текстовом формате, например, CVE-2023-36844 обнаружена в 2023 году)," 
                                    f"solution (text) - Инструкция по устранению уязвимости, description (text) - Описание уязвимости (обычно включает в себя наименования продуктов, программ, технологий, устройств и программного обеспечения, в котором встречается данная уязвимость, и описание места возникновения уязвимости)," 
                                    f"reference (text) - ссылки на источники описывающие уязвимость, cvss (float) - оценка опасности уязвимости. Других полей в таблице нет. Твой запрос должен удовлетворять запросу пользователя. Запрос пользователя: {message.text}. Пришли только запрос, без дополнительного текста и символов." 
                                    f"Не выбирай сразу все поля таблицы. При запрашивании пользователем списка всех уязвимостей или выборки уязвимостей по какому-либо признаку, всегда необходимо выбирать только name из каждой записи, если пользователь не попросил выбрать другое поле." 
                                    f"При использовании оператора LIKE всегда игнорируй регистр строкового выражения и регистр значения поля с помощью функции LOWER(), и используй слова в единственном числе. Например, WHERE LOWER(name) LIKE LOWER('Строковое выражение') Для выборки уязвимостей, которым подвержен продукт ""Название продукта"" необходимо всегда использовать LOWER(description) LIKE LOWER('%Название продукта%').При использовании оператора WHERE с любым из полей, всегда используй функцию LOWER() для этого поля"
                                    f"Для подсчета количества используй функцию COUNT()", 0.6)
        
        ans = ans0.split('```')
        if len(ans)>1:
            req = ans[1]
        else:
            ans1 = ans0.split('`')
            if len(ans1) > 1:
                req = ans1[1]
            else:
                req = ans0
        bot.send_message(message.chat.id, req)
        result = doQuery(req)
        #print(ans0.split('```'))
        if (result!=None):
            strResult = ""
            for item in result:            
                for field in item:
                    strResult=f"{strResult}{field}, "        
                strResult=f"{strResult}\n"
                #strResult = f"{strResult}\n{item}"
            if strResult!="":
                bot.send_message(message.chat.id, strResult[:-3])
                bot.register_next_step_handler(message, get_response)
            else:
                bot.send_message(message.chat.id, f"У меня нет информации по данному запросу. Поменяйте формулировку и попробуйте снова")   
                bot.register_next_step_handler(message, get_response)
                #get_response()
        else:
            bot.send_message(message.chat.id, f"У меня нет информации по данному запросу. Поменяйте формулировку и попробуйте снова")   
            bot.register_next_step_handler(message, get_response)
        
    else:
        bot.send_message(message.chat.id, 'Работа с AI ассистентом приостановлена. Вы можете отправить название уязвимости или воспользоваться командами в нижней панели.')

@bot.message_handler(commands=['updateinfo'])
def main(message):
    bot.send_message(message.chat.id, 'Напишите название уязвимости для проверки информации в открытых источниках')
    bot.register_next_step_handler(message, check)
def check(message):
    cve = CVE.find_info(message.text)
    if type(cve)== CVE:
        bot.send_message(message.chat.id, f'{cve.description}')

#обработка кнопок при вводе названия существующей уязвимости
@bot.message_handler(content_types=['text'])
def answer(message):
    vuln = message.text
    #ans = getSolution(vuln)
    if isExist(vuln):                      
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Описание', callback_data='description'))
        markup.add(types.InlineKeyboardButton('Инструкция по исправлению', callback_data='solution'))
        markup.add(types.InlineKeyboardButton('Ссылки на источники', callback_data='references'))
        
        bot.send_message(message.chat.id, f"{vuln}", reply_markup= markup) 
    else:
        bot.send_message(message.chat.id, f'У меня нет информации по устранению уязвимости "{vuln}". Проверьте правильность написания или перейдите в режим работы с AI ассистентом и попробуйте снова')    

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'description':
        name = callback.message.text
        ans = getDescription(name)
        if ans!=None:
            bot.send_message(callback.message.chat.id, f"{ans}") 
        else:
            bot.send_message(callback.message.chat.id, f'У меня нет информации по уязвимости "{name}". Проверьте правильность написания и попробуйте снова.')    
    elif callback.data == 'solution':
        vuln = callback.message.text
        ans = getSolution(vuln)
        if ans!=None:
            bot.send_message(callback.message.chat.id, f"{ans}") 
        else:
            bot.send_message(callback.message.chat.id, f'У меня нет информации по устранению уязвимости "{vuln}". Проверьте правильность написания и попробуйте снова.')    
    elif callback.data == 'references':
        vuln = callback.message.text
        ans = getReference(vuln)
        if ans!=None:
            bot.send_message(callback.message.chat.id, f"{ans}") 
        else:
            bot.send_message(callback.message.chat.id, f'У меня нет информации по уязвимости "{vuln}". Проверьте правильность написания и попробуйте снова.')    


bot.infinity_polling(timeout=10, long_polling_timeout = 5)
#bot.polling(non_stop=True)