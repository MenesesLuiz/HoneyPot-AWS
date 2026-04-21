Projeto Guardião: HoneyPot em Ambiente AWS

0. Visão Geral

O objetivo deste projeto é criar um ambiente controlado (HoneyPot) para atrair e monitorar tentativas de conexão maliciosas vindas de bots e agentes externos. O sistema é configurado para aceitar tentativas de autenticação que invariavelmente falharão, permitindo a coleta de dados para estudo.

Esta atividade foca no desenvolvimento e integração de competências em:

Linux: Administração de servidores Ubuntu e permissões de sistema.

Python: Automação e manipulação de sockets.

SQL: Modelagem de dados e persistência de logs.

Cibersegurança: Conceitos de monitoramento e análise de ameaças.

Cloud Computing: Provisionamento e configuração de infraestrutura na AWS.

1. Configuração da Infraestrutura

1.1 Instância EC2

O projeto utiliza uma instância t2.micro na AWS com o sistema operacional Ubuntu Server.

1.2 Acesso e Segurança (SSH)

Para estabelecer a conexão via SSH, foi necessário ajustar as permissões da chave privada .pem. O sistema exige que apenas o proprietário tenha acesso de leitura para evitar o erro de vulnerabilidade do arquivo.

Comando de ajuste de permissão:

chmod 400 sua-chave.pem


2. Camada de Dados (MySQL)

O banco de dados armazena os registros de todas as tentativas de intrusão. O status do serviço foi validado através do comando sudo systemctl status mysql.

2.1 Modelagem da Tabela

Dentro da base de dados denominada honeypot, foi criada a tabela registro_ataque com a seguinte estrutura:

CREATE TABLE registro_ataque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip VARCHAR(50),
    usuario VARCHAR(50),
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
);


3. Ambiente de Desenvolvimento Python

3.1 Isolamento de Ambiente (Virtualenv)

Para garantir a integridade do sistema operacional e evitar conflitos entre dependências, foi utilizado um ambiente virtual (env).

3.2 Dependências

A biblioteca necessária para a comunicação entre o script e o banco de dados foi instalada dentro do ambiente isolado:

mysql-connector-python

4. O Script Guardião (guardiao.py)

O arquivo principal, guardiao.py, foi desenvolvido utilizando as seguintes bibliotecas nativas e externas:

Socket: Para escutar e gerenciar conexões TCP na rede.

mysql.connector: Para realizar a inserção dos dados capturados na tabela do MySQL.

5. Configuração de Rede na AWS (Security Group)

Para que o HoneyPot seja acessível externamente, as Regras de Entrada do Security Group foram alteradas para abrir a porta 2222.

Parâmetro

Configuração

Versão IP

IPv4

Tipo

TCP Personalizado

Protocolo

TCP

Intervalo de Portas

2222

Origem

0.0.0.0/0

6. Execução e Monitoramento

Com a infraestrutura provisionada e os serviços configurados, o projeto entra em operação ao executar o script dentro do ambiente virtual:

source .env/bin/activate
python3 guardiao.py


O sistema agora monitora e registra qualquer tentativa de conexão TCP que chegue à porta 2222, alimentando a tabela de logs em tempo real.
