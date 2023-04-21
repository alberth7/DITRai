from pkgutil import get_loader
from Data.VariablesConfiguracion import VariablesConfiguracion
import requests

class Telegram:
    _botToken = str
    _botChatID = str
    _sendText = str

    def __init__(self):
        varpath = VariablesConfiguracion()
        self._botToken = varpath._telegramToken
        self._botChatID = varpath._chatId

    def sendMessage(self, message):
        self._sendText = message
        try:
            send_text = 'https://api.telegram.org/bot' + self._botToken + '/sendMessage?chat_id=' + self._botChatID + '&parse_mode=Markdown&text=' + self._sendText
            #print(send_text)
            response = requests.get(send_text)
            return response.json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
