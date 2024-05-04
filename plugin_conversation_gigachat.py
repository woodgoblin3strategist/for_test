# Болталка с GigaChat.
# Ключ можно получить на https://developers.sber.ru/portal/products/gigachat-api
# author: woodgoblin3strategist


from vacore import VACore
import os

import json #мб нужно для связи с настройками

import requests # туда же
#import gigachain

old_merge_environment_settings = requests.Session.merge_environment_settings

modname = os.path.basename(__file__)[:-3] # calculating modname

authorization_data = "NDdmMzYwOWQtMDIwYS00NjUzLWEzNDEtYTljNjQ3OTExZGIwOmQzMDIxNGVjLWUyMzEtNDI0ZS1hYTc3LWE5MDA4OTY4YjA1ZQ=="

"""Пример работы с чатом через gigachain"""
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
from langchain.callbacks.base import BaseCallbackHandler

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

chat = GigaChat(credentials=authorization_data, verify_ssl_certs=False, streaming=True)

conversation1 = ConversationChain(
    llm = chat,
    verbose=True,
    memory=ConversationBufferMemory()
)

template = '''
Ты являешься доктором исторических наук. Твоя задача красочно и подробно отвечать \
на вопросы по истории. Если задают вопросы по другим темам, говори что это \
тебе не интересно. Не отвечай на вопросы не про историю! Это важно! \
\n\nТекущий разговор:\n{history}\nHuman: {input}\nAI:
'''
conversation1.prompt.template = template

# while(True):
#     user_input = input("User: ")
#     if(user_input == "0"):
#         break
#     res_con = conversation1.predict(input=user_input)
#     print("Bot: ", res_con)

# функция на старте
def start(core:VACore):
    manifest = {
        "name": "Болталка с gigaChat с сохранением контекста",
        "version": "0.1",
        "require_online": True,
        "description": "После указания apiKey позволяет вести диалог с gigaChat.\n"
                       "Голосовая команда: базар|гигачат (для обычной модели с чатом), поясни (для точных фактов)",

        "options_label": {
            "apiKey": "API-ключ gigaChat для доступа к GigaChat", #
            "system": "Вводная строка, задающая характер ответов помощника.",
            "model": "ID нейросетевой модели с сайта Vsegpt",
            "model_spravka": "ID нейросетевой модели с сайта Vsegpt для справок (точных фактов)",
        },

        "default_options": {
            "apiKey": "", #
            "system": "Ты - Ирина, голосовой помощник, помогающий человеку. Давай ответы кратко и по существу.",
            "model": "openai/gpt-3.5-turbo",
            "model_spravka": "perplexity/pplx-70b-online",
            "prompt_tpl_spravka": "Вопрос: {0}. Ответь на русском языке максимально кратко - только запрошенные данные. ",
        },

        "commands": {
            "базар|гигачат": run_start,
            "поясни": run_start_spravka,
        }
    }
    return manifest

def start_with_options(core:VACore, manifest:dict):
    pass

def run_start(core:VACore, phrase:str):

    options = core.plugin_options(modname)

    # if options["apiKey"] == "":
    #     core.play_voice_assistant_speech("Нужен ключ апи для доступа к гигачат точка ру")
    #     return

    # openai.api_key = options["apiKey"]
    # openai.api_base = "https://api.vsegpt.ru:6070/v1"

    new_chat(core)

    if phrase == "":
        core.play_voice_assistant_speech("Да, давай!")
        core.context_set(boltalka, 20)
    else:
        boltalka(core,phrase)

def new_chat(core:VACore):
    options = core.plugin_options(modname)
    # core.chatapp = ChatApp(model=options["model"], system=options["system"])  # создаем новый чат
    core.chatapp = chat



def boltalka(core:VACore, phrase:str):
    if phrase == "отмена" or phrase == "пока":
        core.play_voice_assistant_speech("Пока!")
        return

    if phrase == "новый диалог" or phrase == "новые диалог":
        new_chat(core)
        core.play_voice_assistant_speech("Начинаю новый диалог")
        core.context_set(boltalka, 20)
        return

    try:
        # response = core.chatapp.chat(phrase) #generate_response(phrase)
        # core.say(response["content"])
        # core.context_set(boltalka, 20)
        response = conversation1.predict(input=phrase)
        core.say(response)
        core.context_set(boltalka, 20)
    except:
        import traceback
        traceback.print_exc()
        core.play_voice_assistant_speech("Проблемы с доступом к апи. Посмотрите логи")

        return

# while(True):
#     user_input = input("User: ")
#     if(user_input == "0"):
#         break
#     res_con = conversation1.predict(input=user_input)
#     print("Bot: ", res_con)
