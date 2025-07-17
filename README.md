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

  * [Modelos](#modelos)
  * [Funções Auxiliares](#funções-auxiliares)
  * [Views](#views)
  * [URLs](#urls)
* [Desafio](#desafio)
* [Dependências](#dependências)
* [Contribuição](#contribuição)
* [Licença](#licença)

## Descrição

Este projeto expõe uma API RESTful para operações bancárias básicas:

* **Depósito** em conta existente
* **Saque** com validação de limite diário
* **Consulta de detalhes** da conta
* **Extrato** de operações

Todas as interações ocorrem via requisições HTTP e respostas em JSON.

## Requisitos

* Python 3.8+
* pip
* Django 4.x

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

| Método | URL                              | Descrição                                     |
| ------ | -------------------------------- | --------------------------------------------- |
| POST   | `/core/accounts/deposit/`        | Realiza depósito na conta especificada        |
| POST   | `/core/accounts/withdraw/`       | Realiza saque, valida limite diário de saques |
| GET    | `/core/accounts/<id>/`           | Retorna detalhes da conta                     |
| GET    | `/core/accounts/<id>/statement/` | Retorna extrato (histórico de operações)      |

### Payload (JSON)

Para depósito e saque:

```json
{
  "account_id": 1,
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

O enunciado original encontra-se em \[19 - \[Dio] Desafio.pdf]\(./"19 - \[Dio] Desafio.pdf"). Embora o escopo fosse iniciante, foi implementada validação de limite diário de saque adicional.

## Dependências

* Django>=4.0,<5.0

## Contribuição

1. Faça um fork deste repositório.
2. Crie uma branch para sua feature: `git checkout -b feature/nova-funcionalidade`
3. Commit suas alterações: `git commit -m "Adiciona nova funcionalidade"`
4. Envie para o repositório remoto: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a **MIT License**.
