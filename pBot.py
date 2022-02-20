import requests
from datetime import datetime, date, time
import random
import crc

class pBot():

    ASK_URL = "http://p-bot.ru/api/getAnswer"
    CREATE_DIALOG_URL = "http://p-bot.ru/api/getPatternsCount"

    session = None
    params = {}
    name = ""

    def __init__(self, name):
        self.name = name

        t = crc.unix_time()
        self.params = {"request" : "",
                "request_1" : "",
                "answer_1" : "",
                "request_2" : "",
                "answer_2" : "",
                "request_3" : "",
                "bot_name" : "pBot",
                "user_name" : self.name,
                "dialog_lang" : "ru",
                "dialog_id" : crc.uuidv4(),
                "dialog_greeting" : "False",

                "a" : crc.api(),
                "b" : crc.crc(f"{t}b"),
                "c" : crc.getCRCSign(t),
                "d" : crc.crc(f"{crc.unix_time()}d"),
                "e" : random.random(),
                "t" : t,
                "x" : random.random() * 10}

            
        self.create_chat()


    def ask(self, question):
        self.params["request"] = question 

        js = {}
        response = None
        try:
            response = self.session.post(self.ASK_URL, data = self.params)
            js = response.json()
            answer = js["answer"]
        except Exception as e:
            print("Request error!({0}): {1}".format(e, js))
            return ""

        #bot is saving last three requests and answers
        self.params["request_3"] = self.params["request_2"]
        self.params["answer_3"] = self.params["answer_2"]

        self.params["request_2"] = self.params["request_1"]
        self.params["answer_2"] = self.params["answer_1"]

        self.params["request_1"] = self.params["request"]
        self.params["answer_1"] = answer

        return answer

    def create_chat(self):
        self.session = requests.Session()
        cookies = {"dialog_id": self.params["dialog_id"], "dialog_sentment": "0", "last_visit": "1542708055035::1542718855035" }
        
        js = {}
        response = None
        try:
            response = self.session.get(self.CREATE_DIALOG_URL, cookies = cookies)
            js = response.json() 
        except Exception as e:
            print("Request error!: {0}".format(e))

        if "status" not in js or js["status"] != "OK":
            print("faild to create chat! -> {0}".format(response.content))






