# -*- coding: utf-8 -*-
import socket
import threading
from datetime import datetime


def trata_cliente(conexao, cliente):
    mensagem = conexao.recv(100)
    mensagem = mensagem.decode()

    cont = 0

    with open('Permissoes.json') as mac:
        arquivo = mac.readlines()

    for i in range(len(arquivo)):
        arquivo[i] = arquivo[i].strip('\n')

    for i in arquivo:
        if mensagem == i:
            cont = 1
    if cont == 1:
        texto = "Abrir"
    else:
        texto = 'O Dispositivo {} não está cadastrado!'.format(mensagem)

    btexto = bytes(texto)

    conexao.send(btexto)

    print(texto, "{}".format(datetime.now()))
    conexao.close()


if __name__ == '__main__':
    r = input("Deseja cadastrar ou remover um endereço? \n"
              "Digite c para cadastrar\n"
              "Digite r para remover\n"
              "Digite i inicializar o servidor\n")

    while r != 'i':
        if r == 'c':
            with open('Permissoes.json', 'a') as mac:
                mc = input("Digite o MAC do dispositivo à ser adicionado: \n")
                mac.write("{}\n".format(mc))

            with open('Permissoes.json') as mac:
                arquivo = mac.readlines()
                print(arquivo)

            r = input("Deseja cadastrar ou remover um endereço? \n"
                      "Digite c para cadastrar\n"
                      "Digite r para remover\n"
                      "Digite i inicializar o servidor\n")

        if r == 'r':
            with open('Permissoes.json') as mac:
                arquivo = mac.readlines()

            with open('Permissoes.json', 'w') as mac:
                mc = input("Digite o MAC do dispositivo à ser removido: \n")
                arquivo.remove("{}\n".format(mc))
                print(arquivo)

                for i in arquivo:
                    mac.write(i)

            r = input("Deseja cadastrar ou remover um endereço? \n"
                      "Digite c para cadastrar\n"
                      "Digite r para remover\n"
                      "Digite i inicializar o servidor\n")

print("Iniciando servidor às: {}".format(datetime.now()))
host = ''  # Endereco IP do Servidor
porta = 5003  # Porta que o Servidor esta
soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
origem = (host, porta)
soquete.bind(origem)
soquete.listen(0)

while True:
    tc = threading.Thread(target=trata_cliente, args=soquete.accept())
    tc.start()
