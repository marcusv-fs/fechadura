# -*- coding: utf-8 -*-

from datetime import datetime
import time
import bluetooth
import RPi.GPIO as GPIO
import socket

# variaveis globais
ReleCanal1 = 8  # controle do GPIO23 (este controla o canal 1 do modulo de reles)
ReleCanal2 = 8  # controle do GPIO24 (este controla o canal 2 do modulo de reles)
x = 0
y = 0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)


def mac(arquivo):
	host = ''  # Endereco IP do Servidor
	porta = 5003  # Porta que o Servidor esta
	soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	destino = (host, porta)
	soquete.connect(destino)
	barquivo = bytes(arquivo)
	soquete.send(barquivo)

	arquivo = soquete.recv(100)
	arquivo = arquivo.decode()
	soquete.close()

	if arquivo == "Abrir":  # Aciona rele
		print("Abrindo fechadura, {}".format(datetime.now()))
		GPIO.output(ReleCanal2, GPIO.LOW)
		GPIO.output(ReleCanal1, GPIO.LOW)
		time.sleep(5)

		GPIO.output(ReleCanal1, GPIO.HIGH)
		GPIO.output(ReleCanal2, GPIO.HIGH)

	return arquivo


def search():
	devices = bluetooth.discover_devices(duration=5, lookup_names=True)
	return devices


if __name__ == "__main__":
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(ReleCanal1, GPIO.OUT)
	GPIO.setup(ReleCanal2, GPIO.OUT)

	# desaciona os reles
	GPIO.output(ReleCanal1, GPIO.HIGH)
	GPIO.output(ReleCanal2, GPIO.HIGH)

while True:
	print("[SCAN] Scan BLE sendo realizado. Aguarde...")
	results = search()
	print("[SCAN] Fim do scan BLE.")
	if len(results) > 0:
		for addr, name in results:
			print("Dispositivo encontrado: {0} - {1}".format(addr, name))
			mac(addr)
			y = 0
	else:
		print("Nenhum dispositivo BLE encontrado.")
		y = y + 1
		if y > 4:
			break

	print(results)
	time.sleep(1)
	x = x + 1
	print("Fim do ciclo {}".format(x))

