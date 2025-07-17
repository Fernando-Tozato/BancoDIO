from datetime import datetime

from core.models import Withdrawal, Account


def can_make_withdrawal(account: Account) -> bool:
    withdrawals = Withdrawal.objects.filter(from_account=account)
    withdrawals_today = withdrawals.filter(timestamp__date=datetime.now().date()).count()

    if withdrawals_today >= 3:
        return False
    return True