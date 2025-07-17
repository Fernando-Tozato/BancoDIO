# BancoDIO API

Sistema bancário simples, desenvolvido como exercício de bootcamp da DIO. A aplicação foi implementada apenas como API RESTful usando Django.

## Índice

* [Descrição](#descrição)
* [Requisitos](#requisitos)
* [Instalação](#instalação)
* [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
* [Execução](#execução)
* [Endpoints](#endpoints)
* [Arquitetura do Projeto](#arquitetura-do-projeto)
* [Desafio](#desafio)
* [Dependências](#dependências)
* [Licença](#licença)

## Descrição

Este projeto expõe uma API RESTful para operações bancárias básicas:

* **Depósito** em conta existente
* **Saque** com validação de limite diário
* **Transferência** entre contas diferentes
* **Consulta de detalhes** da conta
* **Extrato** de operações

Todas as interações ocorrem via requisições HTTP e respostas em JSON.

## Requisitos

* Python 3.8+
* pip
* Django 5.x

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/Fernando-Tozato/BancoDIO.git
   cd BancoDIO
   ```
2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Configuração do Banco de Dados

Por padrão, o projeto usa SQLite. Para alterar o banco, edite `BancoDIO/settings.py` na seção `DATABASES`.

## Execução

Aplique migrações e inicialize o servidor Django:

```bash
python manage.py migrate
python manage.py runserver
```

A API ficará disponível em `http://127.0.0.1:8000/`.

## Endpoints

| Método | URL                                 | Descrição                                               |
| ------ |-------------------------------------|---------------------------------------------------------|
| POST   | `/core/deposit/`                    | Realiza depósito na conta especificada                  |
| POST   | `/core/withdraw/`                   | Realiza saque, valida limite diário de saques           |
| POST   | `/core/transfer/`                   | Realiza transferência, valida se as duas contas existem |
| GET    | `/core/statement/<account_number>/` | Retorna extrato (histórico de operações)                |
| GET    | `/core/accounts/`                   | Retorna detalhes de todas as contas                     |
| GET    | `/core/account/<account_number>/`   | Retorna detalhes de todas as contas                     |


### Payload (JSON)

Depósito:
```json
{
  "to_account": 1,
  "amount": 150.00
}
```
\
Saque:
```json
{
  "from_account": 1,
  "amount": 150.00
}
```
\
Transferência:
```json
{
  "from_account": 1,
  "to_account": 2,
  "amount": 150.00
}
```

## Arquitetura do Projeto

### Modelos (`core/models.py`)

* **Account**: campos `id`, `account_number` (CharField), `balance` (DecimalField).
* **Operation**: campos `id`, `account` (ForeignKey para Account), `type` (choices: DEPOSIT ou WITHDRAW), `amount` (DecimalField), `timestamp` (DateTimeField auto\_now\_add).

### Funções Auxiliares (`core/functions.py`)

* **can\_make\_withdrawal(account, amount)**: verifica quantidade de saques já realizados no dia e se o valor solicitado não ultrapassa o limite diário.

### Views (`core/views.py`)

Views baseadas em função que:

* Validam entrada (presença de `account_id` e `amount`, valores positivos).
* Verificam existência da conta.
* Chamam helpers para depósito ou saque.
* Retornam `JsonResponse` com status HTTP adequados.

### URLs

* `BancoDIO/urls.py`: inclui as rotas de `core/urls.py`.
* `core/urls.py`: define rotas para cada operação de API.

## Desafio

O enunciado original encontra-se em [Desafio DIO.pdf](./"Desafio%20DIO.pdf").

## Dependências

* Django>=5.0

## Licença

Este projeto está licenciado sob a [**MIT License**](./LICENSE).
