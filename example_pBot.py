import pBot

pbot = pBot.pBot("anonym")

msg = input("Введите сообщение: ")
while msg != "exit":

    print("pBot: {0}".format(pbot.ask(msg)))
    msg = input("Вы: ")
