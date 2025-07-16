from django.db import models
from django.db.models import enums

class Account(models.Model):
    account_number = models.CharField(max_length=20, unique=True, verbose_name="Account Number")
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, verbose_name="Balance")

    def __str__(self):
        return f"Account {self.account_number} - Balance: {self.balance}"

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"


class OperationsType(enums.TextChoices):
    TRANSFER = 'T', 'Transfer'
    DEPOSIT = 'D', 'Deposit'
    WITHDRAWAL = 'W', 'Withdrawal'

class OperationsWay(enums.TextChoices):
    IN = 'IN', 'In'
    OUT = 'OUT', 'Out'
    IN_OUT = 'IN_OUT', 'In/Out'

class Operation(models.Model):
    type = models.CharField(max_length=10, choices=OperationsType.choices)
    way = models.CharField(max_length=10, choices=OperationsWay.choices)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    timestamp = models.DateTimeField(auto_now_add=True)
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfer_from', verbose_name="From Account", null=True, blank=True)
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfer_to', verbose_name="To Account", null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp.strftime('%d/%m/%Y %H:%M:%S')} - {self.get_type_display()} - {self.get_way_display()} - {self.amount}"

    def save(self, **kwargs):
        if self.type == OperationsType.DEPOSIT:
            self.from_account = None
            self.way = OperationsWay.IN
            self.to_account.balance += self.amount
            self.to_account.save()

        elif self.type == OperationsType.WITHDRAWAL:
            self.to_account = None
            self.way = OperationsWay.OUT
            self.from_account.balance -= self.amount
            self.from_account.save()

        else:
            if self.from_account is None or self.to_account is None:
                raise ValueError("Both from_account and to_account must be set for transfers.")


            self.way = OperationsWay.IN_OUT

            self.from_account.balance -= self.amount
            self.from_account.save()

            self.to_account.balance += self.amount
            self.to_account.save()

        super().save()

    class Meta:
        verbose_name = "Operation"
        verbose_name_plural = "Operations"

class Deposit(Operation):
    type = OperationsType.DEPOSIT
    way = OperationsWay.IN

    class Meta:
        verbose_name = "Deposit"
        verbose_name_plural = "Deposits"

class Withdrawal(Operation):
    type = OperationsType.WITHDRAWAL
    way = OperationsWay.OUT

    class Meta:
        verbose_name = "Withdrawal"
        verbose_name_plural = "Withdrawals"

class Transfer(Operation):
    type = OperationsType.TRANSFER
    way = OperationsWay.IN_OUT

    class Meta:
        verbose_name = "Transfer"
        verbose_name_plural = "Transfers"