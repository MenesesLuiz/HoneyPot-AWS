import socket
import mysql.connector
from datetime import datetime

print("Iniciando Guardiao")


try:
    banco = mysql.connector.connect(
        host="localhost",
        user="meuusuario",
        password="minhasenha",
        database="honeypot"
    )
    cursor = banco.cursor()
    print("Conectado ao banco de dados")
except Exception as e:
    print(f"Erro ao conectar no banco: {e}")

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('0.0.0.0', 2222))
servidor.listen(5)

while True:
    conexao, endereco = servidor.accept()
    ip_atacante = endereco[0]

    print(f"Invasor detectado! IP: {ip_atacante}")

    try:
        sql = "INSERT INTO registro_ataques (ip, usuario) VALUES (%s, %s)"
        valores = (ip_atacante, "bot_varredura")
        cursor.execute(sql, valores)
        banco.commit()
    except:
        pass

    conexao.send(b"Ubuntu 22.04 LTS - Login: \n")
    conexao.close()
