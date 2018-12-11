from urllib.parse import urlencode
from urllib.request import Request, urlopen
from datetime import datetime, date, time
import sys
import random
import json
import crc

class pBot(object):

    params = {}
    name = ""

    def __init__(self, name):
        self.name = name

    def Init(self):
        self.InitParams()
        return self.CreateChat()

    def Ask(self, request):

        url = 'http://p-bot.ru/api/getAnswer'
        
        self.params["request"] = request

        request = Request(url, urlencode(self.params).encode())

        stat_code = 0
        html = ""
        
        request.add_header('Cookie','{0}={1}; {2}={3}; {4}={5}'.\
                format("dialog_id", self.params["dialog_id"],\
                       "dialog_sentiment", "0", \
                       "last_visit", "1542708055035::1542718855035"))


        try:
            r = urlopen(request)
            html = r.read().decode()
            status_code = r.getcode()

            js = json.loads(html)
            answer = js["answer"]
        except Exception as e:
            print("Request error!({0}): {1}".format(e, html))
            return ""

        #bot saved last three request and answer
        #save last request and answer
        self.params["request_3"] = self.params["request_2"]
        self.params["answer_3"] = self.params["answer_2"]

        self.params["request_2"] = self.params["request_1"]
        self.params["answer_2"] = self.params["answer_1"]

        self.params["request_1"] = self.params["request"]
        self.params["answer_1"] = answer

        return answer

    def CreateChat(self):
        url = 'http://p-bot.ru/api/getPatternsCount' 

        stat_code = 0
        html = ""

        request = Request(url)

        #Cookies
        request.add_header('Cookie','{0}={1}; {2}={3}; {4}={5}'.\
                format("dialog_id", self.params["dialog_id"],\
                       "dialog_sentiment", "0", \
                       "last_visit", "1542708055035::1542718855035"))

        #Connect and request
        try:
            r = urlopen(request)
            html = r.read().decode()
            status_code = r.getcode()
            js = json.loads(html)
        except Exception as e:
            print("Request error!: {0}".format(e))
            return False

        if "status" not in js or js["status"] != "OK":
            print("Impossible to create chat! -> {0}".format(html))
            return False

        return True 

    def InitParams(self):
        #get unix_time
        y4 = int(crc.unix_time(datetime.today()) * 1000) - 10000000
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
                "b" : crc.crc(str(y4) + 'b'),
                "c" : crc.getCRCSign(y4),
                "d" : crc.crc(str(int(crc.unix_time(datetime.today()) * 1000) ) + 'd'),
                "e" : random.random(),
                "t" : y4,
                "x" : random.random() * 10}







