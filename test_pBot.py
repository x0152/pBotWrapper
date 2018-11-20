import pBot

pbot = pBot.pBot("Егор")

pbot.Init()

msg = input("Введите сообщение: ")
while msg != "exit":

    print("pBot: {0}".format(pbot.Ask(msg)))
    msg = input("Вы: ")
