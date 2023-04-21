import schedule
import time
import sys

from BusinessLogic.AgenteAnalizador import AgenteAnalizador
from BusinessLogic.Telegram import Telegram
from Data.VariablesConfiguracion import VariablesConfiguracion


def notificacionDeInicio(frecuency):
    telegram = Telegram()
    message = f'''
----------------------------------------------------------
***Se inicio el Software Agente Inteligente DITRAI 🤖 !!!***
\nNosotros cuidaremos su seguridad en la red de Internet.
\nSu red tráfico de red será analizado cada {frecuency} minutos.
\nAtte.: DITRai 🤖

---------------------------------------------------------
'''
    #print(message)
    telegram.sendMessage(message)

def job():
    try:
        telegram = Telegram()
        agente_Analizador = AgenteAnalizador()

        agente_Analizador.objetivoSolicitar()
        agente_Analizador.objetivoDetectar()
        agente_Analizador.objetivoBloquear()
        agente_Analizador.actualizarTablas()

        telegram.sendMessage("El Agente Inteligente **DITRai** se esta ejecutando sin problemas!!!")
    except Exception as e:
        print(e)
        telegram = Telegram()
        telegram.sendMessage('Error en la ejecución del Agente Inteligente **DITRai**:')
        telegram.sendMessage(str(e).replace("_", "+"))
        sys.exit()


if __name__ == '__main__':
    print(">>>>>> AGENTE INTELIGENTE DITRai INICIADO <<<<<<")
    varConf = VariablesConfiguracion()
    frecuencyDeMonitoreo = varConf._monitorSystem
    notificacionDeInicio(frecuencyDeMonitoreo)
    job()
    schedule.every(frecuencyDeMonitoreo).minutes.do(job)

    while True:
        try:
            schedule.run_pending()
            print(">>>>>> PROCESO DE ANANLISIS FINALIZADO <<<<<<")
            time.sleep(1)
            #print("time")

        except Exception as e:
            print(e)
            telegram = Telegram()
            telegram.sendMessage('Error en la ejecución del AGENTE INTELIGENTE DITRai:')
            telegram.sendMessage(str(e).replace("_", "+"))
            sys.exit()

