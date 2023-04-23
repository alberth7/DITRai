import time
import requests
import sys

from datetime import datetime
from datetime import timedelta
from router import Router
from dataRouterInDB import DataRouterInDB
from telegram import Telegram

if __name__ == '__main__':
    telegram = Telegram()
    router = Router()
    dataRouterInDB = DataRouterInDB()

    timeSleep = 3
    everyMinuteSendMessage = 30
    sw = 0

    telegram.sendMessage("El sistema se inicio con extitos!!!")
    while True:
        try:
            router.getContrackXML_and_DHCP()
            dataRouterInDB.saveDataInPostgresql()
            time.sleep(timeSleep)

            timeNow = datetime.now()
            if sw == 0:
                timeSenMessage = timeNow + timedelta(minutes = everyMinuteSendMessage)
                sw = 1
            if timeNow.hour == timeSenMessage.hour and timeNow.minute == timeSenMessage.minute and sw == 1:
                telegram.sendMessage("El sistema se esta ejecutando sin problemas!!!")
                sw = 0

        except Exception as e:
            telegram.sendMessage('Error en el sistema:')
            telegram.sendMessage(str(e).replace("_","+"))
            sys.exit()




