import logging
import os
import socket
import sys

import mysql.connector
from mysql.connector import Error


HOST = os.getenv("HONEYPOT_HOST", "0.0.0.0")
PORT = int(os.getenv("HONEYPOT_PORT", "2222"))
BACKLOG = int(os.getenv("HONEYPOT_BACKLOG", "50"))
BANNER = os.getenv("HONEYPOT_BANNER", "Ubuntu 22.04 LTS - Login: \n").encode("utf-8")

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE", "honeypot"),
}

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("guardiao")


def conectar_banco():
    """Abre uma conexão com o MySQL ou encerra o serviço com uma mensagem clara."""
    if not DB_CONFIG["user"] or not DB_CONFIG["password"]:
        raise RuntimeError("Defina MYSQL_USER e MYSQL_PASSWORD antes de iniciar o serviço.")

    try:
        conexao = mysql.connector.connect(**DB_CONFIG)
        logger.info("Conectado ao banco de dados")
        return conexao
    except Error as erro:
        raise RuntimeError(f"Não foi possível conectar ao MySQL: {erro}") from erro


def registrar_ataque(banco, ip_atacante):
    """Registra uma conexão recebida; reconecta uma vez se o MySQL cair."""
    try:
        if not banco.is_connected():
            banco.reconnect(attempts=1, delay=0)

        cursor = banco.cursor()
        try:
            cursor.execute(
                "INSERT INTO registro_ataques (ip, usuario) VALUES (%s, %s)",
                (ip_atacante, "conexao_tcp"),
            )
            banco.commit()
        finally:
            cursor.close()
    except Error as erro:
        logger.error("Não foi possível registrar a conexão de %s: %s", ip_atacante, erro)
        try:
            banco.rollback()
        except Error:
            pass


def atender_conexao(conexao, endereco, banco):
    ip_atacante = endereco[0]
    logger.warning("Conexão recebida de %s", ip_atacante)
    registrar_ataque(banco, ip_atacante)

    try:
        conexao.settimeout(5)
        conexao.sendall(BANNER)
    except OSError as erro:
        logger.info("Cliente %s desconectou antes do banner: %s", ip_atacante, erro)
    finally:
        conexao.close()


def main():
    try:
        banco = conectar_banco()
    except RuntimeError as erro:
        logger.error(erro)
        return 1

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        servidor.bind((HOST, PORT))
        servidor.listen(BACKLOG)
        logger.info("Guardião escutando em %s:%s", HOST, PORT)

        while True:
            conexao, endereco = servidor.accept()
            atender_conexao(conexao, endereco, banco)
    except KeyboardInterrupt:
        logger.info("Guardião encerrado pelo operador")
    except OSError as erro:
        logger.error("Falha no servidor TCP: %s", erro)
        return 1
    finally:
        servidor.close()
        if banco.is_connected():
            banco.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
