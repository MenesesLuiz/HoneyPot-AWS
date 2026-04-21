0. HoneyPot utilizando AWS

O objetivo do projeto é criar um ambiente onde bots possam tentar se conectar à minha instância por meio de senhas (e falharão). Nessa atividade irei enriquecer meus conhecimentos em Linux, Python, SQL, Cibersegurança e (obviamente) Cloud.

1. Criando a instância

Nesse projeto estarei utilizando um Ubuntu Server numa instância EC2 na AWS de tipo t2.micro.

1.1. Realizando a conexão via SSH

Após salvar minha chave de acesso SSH .pem eu tive que alterar as configurações de permissões, permitindo apenas o meu usuário ler a chave para poder conectar no servidor sem dar o erro de "UNPROTECTED PRIVATE KEY FILE".

1.2. Instalação do MySQL e criação das tabelas

Ele vai servir principalmente para armazenar os logs do nosso HoneyPot. após a instalação, chequei pra ver se o processo estava rodando tudo certinho com o comando: sudo systemctl status mysql. Após concluir a instalação e verificar que o MySQL está OK, entrei no banco de dados e criei a tabela honeypot, dentro dela rodei o script:

CREATE TABLE registro_ataque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip VARCHAR(50),
    usuario VARCHAR(50),
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
);


1.3. Instalação do Python e suas bibliotecas

Como utilizaremos bibliotecas do Python, o sistema não permite que instalemos qualquer coisa, precisei instalar o env do python para isolar ele do meu ambiente.
Após entrar na env, instalei a biblioteca mysql-connector-python.

1.4. Script guardiao.py

Entrando na .env, criamos o arquivo guardiao.py que irá armazenar o meu script em python, o script utiliza a biblioteca socket e mysql.connector.

1.5. Configuração na AWS

Antes de tudo, precisamos alterar o security group na AWS para abrir a porta 2222 para qualquer conexão TCP. Para isso alteramos as regras de entrada:

Versão do IP: IPv4

Tipo: TCP Personalizado

Protocolo: TCP

Intervalo de portas: 2222

Origem: 0.0.0.0/0

2.0 Tudo pronto

Após as configurações do nosso humilde projeto estarem feitas com o banco de dados ok, script ok e tudo configurado como deve ser. Rodamos o guardiao.py (o arquivo do nosso script) no nosso .env para pegarmos qualquer conexão TCP que tenta chegar na porta 2222
