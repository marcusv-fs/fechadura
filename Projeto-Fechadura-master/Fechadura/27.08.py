import time
import bluetooth
import RPi.GPIO as GPIO
from datetime import datetime

# variaveis globais
MACPermitido1 = ""  # endereco MAC de um dispositivo que devera acionar um dos canais do modulo de rele
MACPermitido2 = ""  # endereco MAC de um dispositivo que devera acionar um dos canais do modulo de rele
ReleCanal1 = 8  # controle do GPIO23 (este controla o canal 1 do modulo de reles)
ReleCanal2 = 8  # controle do GPIO24 (este controla o canal 2 do modulo de reles)
#x = 0
y = 0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)


# Implementacoes

# Funcao: verifica se alguma acao deve ser tomada para algum dispositivo encontrado
# Parametros: endereco MAC do dispositivo encontrado
# Retorno: nenhum
def VerificaDispositivosLista(MACDisp):
    global MACPermitido1
    global MACPermitido2
    DispositivoPermitidoDetectado = 0

    if MACDisp == MACPermitido1:
        # dispositivo encontrado. Dispara acao correspondente
        DispositivoPermitidoDetectado = DispositivoPermitidoDetectado + 1

    if MACDisp == MACPermitido2:
        # dispositivo encontrado. Dispara acao correspondente
        DispositivoPermitidoDetectado = DispositivoPermitidoDetectado + 1

    if DispositivoPermitidoDetectado > 0:  # Aciona rele
        GPIO.output(ReleCanal2, GPIO.LOW)
        time.sleep(5)

        GPIO.output(ReleCanal1, GPIO.HIGH)
        GPIO.output(ReleCanal2, GPIO.HIGH)

    return


def search():
    devices = bluetooth.discover_devices(duration=2, lookup_names=True)
    return devices


if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ReleCanal1, GPIO.OUT)
    GPIO.setup(ReleCanal2, GPIO.OUT)

    # desaciona os reles
    GPIO.output(ReleCanal1, GPIO.HIGH)
    GPIO.output(ReleCanal2, GPIO.HIGH)

while True:
    results = search()
    if len(results) > 0:
        print("Abrindo fechadura: horario {}".format(datetime.now()))
        y = 0
        for addr, name in results:
            VerificaDispositivosLista(addr)
    else:
        print("Nenhum dispositivo BLE encontrado: horario {}".format(datetime.now()))
        y = y + 1
        if y > 4:
            break
