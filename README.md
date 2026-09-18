# Honeypot TCP na AWS

Um sensor TCP simples para registrar conexões recebidas em uma porta exposta de uma instância EC2. A cada conexão, o serviço grava o IP, data/hora e o tipo de evento no MySQL, envia um banner e encerra a sessão.

> Este projeto **não implementa SSH** e não captura credenciais. Um cliente SSH na porta 2222 falhará na negociação porque o serviço é TCP simples. Não exponha o SSH administrativo da instância à internet; mantenha-o em outra porta ou restrinja-o ao seu IP no Security Group.

## Pré-requisitos

- Ubuntu Server em uma instância EC2
- Python 3.10 ou superior
- MySQL Server
- Regra de entrada TCP para a porta escolhida (por padrão, `2222`)

## Instalação

Clone o repositório, crie o ambiente virtual e instale a dependência:

```bash
git clone https://github.com/SEU_USUARIO/HoneyPot-AWS.git
cd HoneyPot-AWS
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Crie o banco e a tabela:

```bash
sudo mysql < bd.sql
```

Crie um usuário MySQL com acesso apenas ao banco do projeto. Escolha uma senha forte no lugar de `SUA_SENHA`:

```sql
CREATE USER 'honeypot_app'@'localhost' IDENTIFIED BY 'SUA_SENHA';
GRANT INSERT ON honeypot.registro_ataques TO 'honeypot_app'@'localhost';
FLUSH PRIVILEGES;
```

Configure as variáveis de ambiente sem versionar segredos:

```bash
cp .env.example .env
nano .env
set -a
source .env
set +a
```

Inicie manualmente para testar:

```bash
python guardiao.py
```

Em outro terminal, teste uma conexão:

```bash
nc -v IP_DA_INSTANCIA 2222
```

Consulte os eventos:

```sql
SELECT id, ip, usuario, data_hora
FROM registro_ataques
ORDER BY data_hora DESC;
```

## Execução como serviço

O arquivo `guardiao.service` mantém o processo ativo após logout ou reinicialização. Ajuste os caminhos e o usuário `honeypot` se necessário, depois execute:

```bash
sudo cp guardiao.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now guardiao
sudo systemctl status guardiao
```

Use `journalctl -u guardiao -f` para acompanhar os logs.

## Segurança e limites

- Mantenha `.env` privado; ele contém a senha do banco.
- Use um usuário MySQL exclusivo e com permissão mínima de `INSERT`.
- A porta pública receberá tráfego não confiável. Rode este serviço em uma instância isolada, sem dados pessoais ou outros serviços expostos.
- Registros de IP podem estar sujeitos a requisitos de privacidade e retenção. Defina uma política de descarte adequada ao seu contexto.
