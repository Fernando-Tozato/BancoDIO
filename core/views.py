import json

from django.db.models import Q
from django.db.models.functions import TruncDate
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from core.functions import can_make_withdrawal
from core.models import Deposit, Account, Withdrawal, OperationsType, OperationsWay, Transfer, Operation


@csrf_exempt
def deposit(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body.decode('utf-8'))
    amount = data.get('amount')
    to_account = Account.objects.filter(account_number=data.get('to_account')).first()

    print(f"Received deposit request: Amount={amount}, To account={to_account}")

    if amount is None or to_account is None:
        return JsonResponse({'error': 'Invalid request data'}, status=400)

    if amount <= 0:
        return JsonResponse({'error': 'Amount must be greater than zero'}, status=400)

    new_deposit = Deposit(
        type=OperationsType.DEPOSIT,
            way=OperationsWay.IN,
        amount=amount,
        to_account=to_account,
    )
    new_deposit.save()

    return JsonResponse({'success': 'Deposit successful'}, status=201)

@csrf_exempt
def withdrawal(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body.decode('utf-8'))
    amount = data.get('amount')
    from_account = Account.objects.filter(account_number=data.get('from_account')).first()

    print(f"Received withdrawal request: Amount={amount}, From account={from_account}")

    if amount is None or from_account is None:
        return JsonResponse({'error': 'Invalid request data'}, status=400)

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

    return HttpResponse(request)

@csrf_exempt
def transfer(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body.decode('utf-8'))
    amount = data.get('amount')
    from_account = Account.objects.filter(account_number=data.get('from_account')).first()
    to_account = Account.objects.filter(account_number=data.get('to_account')).first()

    print(f"Received withdrawal request: Amount={amount}, From account={from_account}, To account={to_account}")

    if amount is None or from_account is None or to_account is None:
        return JsonResponse({'error': 'Invalid request data'}, status=400)

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

    return HttpResponse(request)


def make_statement(request, account_number):
    account = Account.objects.filter(account_number=account_number).first()

    if account is None:
        return JsonResponse({'error': 'Conta não encontrada'}, status=404)

    statement_data = []

    operations = Operation.objects.filter(Q(from_account=account) | Q(to_account=account)).order_by('timestamp')

    date_list = operations.annotate(date_only=TruncDate('timestamp')).values_list('date_only', flat=True).distinct().order_by('date_only')

    for date in date_list:
        date_formatted = date.strftime('%d/%m/%Y')
        daily_operations = operations.filter(timestamp__date=date)
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

def accounts(request):
    accounts_list = Account.objects.all()

    data = []
    for account in accounts_list:
        data.append({
            'account_number': account.account_number,
            'balance': float(account.balance),
        })

    return JsonResponse(data, safe=False)

def account_detail(request, account_number):
    account = Account.objects.filter(account_number=account_number).first()

    if account is None:
        return JsonResponse({'error': 'Conta não encontrada'}, status=404)

    data = {
        'account_number': account.account_number,
        'balance': float(account.balance)
    }

    return JsonResponse(data)
