import json
from datetime import datetime

from django.db.models import Q
from django.db.models.functions import TruncDate
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from core.functions import can_make_withdrawal, is_cpf_valid
from core.models import Deposit, Account, Withdrawal, OperationsType, OperationsWay, Transfer, Operation, Client

'''
    OPERATIONS
'''
@csrf_exempt
def make_deposit(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body.decode('utf-8'))
    amount = data.get('amount')
    to_account = Account.objects.filter(account_number=data.get('to_account')).first()

    print(f"Received deposit request: Amount={amount}, To account={to_account}")

    if amount is None or to_account is None:
        return JsonResponse({'error': 'Invalid request data'}, status=400)

    if not to_account.is_active:
        return JsonResponse({'error': 'Account is inactive'}, status=400)

    if amount <= 0:
        return JsonResponse({'error': 'Amount must be greater than zero'}, status=400)

    new_deposit = Deposit(
        type=OperationsType.DEPOSIT,
        way=OperationsWay.IN,
        amount=amount,
        to_account=to_account,
    )
    new_deposit.save()

    return JsonResponse({'success': 'Deposit successful', 'balance': to_account.balance}, status=201)

@csrf_exempt
def make_withdrawal(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body.decode('utf-8'))
    amount = data.get('amount')
    from_account = Account.objects.filter(account_number=data.get('from_account')).first()

    print(f"Received withdrawal request: Amount={amount}, From account={from_account}")

    if amount is None or from_account is None:
        return JsonResponse({'error': 'Invalid request data'}, status=400)

    if not from_account.is_active:
        return JsonResponse({'error': 'Account is inactive'}, status=400)

    if amount <= 0:
        return JsonResponse({'error': 'Amount must be greater than zero'}, status=400)

    if amount > 500:
        return JsonResponse({'error': 'Withdrawal amount exceeds limit of 500'}, status=400)

    if amount > from_account.balance:
        return JsonResponse({'error': 'Insufficient funds'}, status=400)

    if not can_make_withdrawal(from_account):
        return JsonResponse({'error': 'Withdrawal limit exceeded for today'}, status=400)

    new_withdrawal = Withdrawal(
        type=OperationsType.WITHDRAWAL,
        way=OperationsWay.OUT,
        amount=amount,
        from_account=from_account,
    )
    new_withdrawal.save()

    return JsonResponse({'success': 'Withdrawal successful', 'balance': from_account.balance}, status=201)

@csrf_exempt
def make_transfer(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body.decode('utf-8'))
    amount = data.get('amount')
    from_account = Account.objects.filter(account_number=data.get('from_account')).first()
    to_account = Account.objects.filter(account_number=data.get('to_account')).first()

    print(f"Received transfer request: Amount={amount}, From account={from_account}, To account={to_account}")

    if amount is None or from_account is None or to_account is None:
        return JsonResponse({'error': 'Invalid request data'}, status=400)

    if not from_account.is_active or not to_account.is_active:
        return JsonResponse({'error': 'One or both accounts are inactive'}, status=400)

    if amount <= 0:
        return JsonResponse({'error': 'Amount must be greater than zero'}, status=400)

    if amount > from_account.balance:
        return JsonResponse({'error': 'Insufficient funds'}, status=400)

    new_transfer = Transfer(
        type=OperationsType.TRANSFER,
        way=OperationsWay.IN_OUT,
        amount=amount,
        from_account=from_account,
        to_account=to_account,
    )
    new_transfer.save()

    return JsonResponse({'success': 'Transfer successful', 'from_account_balance': from_account.balance}, status=201)

def get_statement(request, account_number):
    account = Account.objects.filter(account_number=account_number).first()

    if account is None:
        return JsonResponse({'error': 'Account not found'}, status=404)

    if not account.is_active:
        return JsonResponse({'error': 'Account is inactive'}, status=400)

    statement_data = []

    operations_filtered = Operation.objects.filter(Q(from_account=account) | Q(to_account=account))

    date_list = operations_filtered.annotate(date_only=TruncDate('timestamp')).values_list('date_only', flat=True).distinct().order_by('date_only')

    for date in date_list:
        date_formatted = date.strftime('%d/%m/%Y')
        daily_operations = operations_filtered.filter(timestamp__date=date)
        daily_data = {
            'date': date_formatted,
            'operations': []
        }

        for operation in daily_operations:
            operation_data = {
                'time': operation.timestamp.strftime('%H:%M:%S'),
                'type': operation.get_type_display(),
                'way': operation.get_way_display(),
                'amount': f'R${float(operation.amount):.2f}',
                'balance': f'R${float(account.balance):.2f}',
            }
            if operation.from_account != account and operation.from_account is not None:
                operation_data['from_account'] = operation.from_account.account_number
            if operation.to_account != account and operation.to_account is not None:
                operation_data['to_account'] = operation.to_account.account_number

            daily_data['operations'].append(operation_data)
        statement_data.append(daily_data)

    return JsonResponse({'success': 'Statement retrieved successfully', 'statement': statement_data}, status=200)

'''
    ACCOUNTS
'''
def get_accounts(request, client_cpf=None):
    if client_cpf:
        if not is_cpf_valid(client_cpf):
            return JsonResponse({'error': 'Invalid CPF'}, status=400)

        client = Client.objects.filter(cpf=client_cpf).first()

        if not client:
            return JsonResponse({'error': 'Client not found'}, status=404)

        accounts_filtered = Account.objects.filter(client=client)
    else:
        accounts_filtered = Account.objects.all()

    data = {
        'accounts': [account.__str__() for account in accounts_filtered],
        'count': accounts_filtered.count(),
    }

    return JsonResponse({'success': 'Accounts retrieved successfully', 'data': data})

def get_account_details(request, account_number):
    account = Account.objects.filter(account_number=account_number).first()

    if account is None:
        return JsonResponse({'error': 'Account not found'}, status=404)

    data = {
        'agency_number': account.agency_number,
        'account_number': account.account_number,
        'balance': float(account.balance),
        'client_cpf': account.client.cpf,
        'client_name': account.client.name,
    }

    return JsonResponse({'success': 'Account details retrieved successfully', 'data': data})

@csrf_exempt
def create_account(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body.decode('utf-8'))
    client_cpf = data.get('client_cpf')
    account_number = data.get('account_number')

    if not client_cpf or not account_number:
        return JsonResponse({'error': 'Client CPF and account number are required'}, status=400)

    if not is_cpf_valid(client_cpf):
        return JsonResponse({'error': 'Invalid CPF'}, status=400)

    client = Client.objects.filter(cpf=client_cpf).first()

    if not client:
        return JsonResponse({'error': 'Client not found'}, status=404)

    if account_number in [account.account_number for account in Account.objects.all()]:
        return JsonResponse({'error': 'Account with this number already exists'}, status=400)

    new_account = Account(
        account_number=account_number,
        client=client
    )
    new_account.save()

    return JsonResponse({'success': 'Account created successfully', 'account_number': new_account.account_number}, status=201)

def inactivate_account(request, account_number):
    account = Account.objects.filter(account_number=account_number).first()

    if account is None:
        return JsonResponse({'error': 'Account not found'}, status=404)

    account.is_active = False
    account.save()

    return JsonResponse({'success': 'Account deactivated successfully'}, status=200)

def activate_account(request, account_number):
    account = Account.objects.filter(account_number=account_number).first()

    if account is None:
        return JsonResponse({'error': 'Account not found'}, status=404)

    account.is_active = True
    account.save()

    return JsonResponse({'success': 'Account activated successfully'}, status=200)


'''
    CLIENTS
'''
def get_client(request, client_cpf):
    if not is_cpf_valid(client_cpf):
        return JsonResponse({'error': 'Invalid CPF'}, status=400)

    client = Client.objects.filter(cpf=client_cpf).first()

    if not client:
        return JsonResponse({'error': 'Client not found'}, status=404)

    data = {
        'name': client.name,
        'cpf': client.formatted_cpf(),
        'accounts': [account.__str__() for account in Account.objects.filter(client=client)],
    }

    return JsonResponse({'success': 'Client details retrieved successfully', 'data': data})

@csrf_exempt
def create_client(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body.decode('utf-8'))
    name = data.get('name')
    cpf = data.get('cpf')
    birth_date = data.get('birth_date')
    street_address = data.get('street_address')
    street_number = data.get('street_number')
    neighborhood = data.get('neighborhood')
    city = data.get('city')
    state_code = data.get('state_code')

    if not all([name, cpf, birth_date, street_address, street_number, neighborhood, city, state_code]):
        return JsonResponse({'error': 'All fields are required'}, status=400)

    if not is_cpf_valid(cpf):
        return JsonResponse({'error': 'Invalid CPF'}, status=400)

    clients = Client.objects.all()

    if clients.count() > 0:
        if cpf in [client.cpf for client in clients]:
            return JsonResponse({'error': 'Client with this CPF already exists'}, status=400)

    new_client = Client(
        name=name,
        cpf=cpf,
        birth_date=datetime.strptime(birth_date, '%d/%m/%Y').date(),
        street_address=street_address,
        street_number=street_number,
        neighborhood=neighborhood,
        city=city,
        state_code=state_code
    )
    new_client.save()

    return JsonResponse({'success': 'Client created successfully', 'client_cpf': new_client.cpf}, status=201)