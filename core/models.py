from django.db import models
from django.db.models import enums


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="Client Name")
    birth_date = models.DateField(verbose_name="Birth Date")
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    street_address = models.CharField(max_length=255, verbose_name="Street Address")
    street_number = models.CharField(max_length=10, verbose_name="Street Number")
    neighborhood = models.CharField(max_length=100, verbose_name="Neighborhood")
    city = models.CharField(max_length=100, verbose_name="City")
    state_code = models.CharField(max_length=2, verbose_name="State Code")

    def formatted_address(self):
        return f"{self.street_address}, {self.street_number} - {self.neighborhood} - {self.city}/{self.state_code}"

    def formatted_cpf(self):
        return f"{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}"

    def __str__(self):
        return f"{self.name} - {self.formatted_cpf()}"

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

class Account(models.Model):
    account_number = models.CharField(max_length=20, unique=True, verbose_name="Account Number")
    agency_number = models.CharField(max_length=10, verbose_name="Agency Number", default='0001')
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, verbose_name="Balance")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='accounts', verbose_name="Client")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    def __str__(self):
        return f"{self.agency_number} - {self.account_number}"

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
        return f"{self.get_type_display()} - {self.timestamp.strftime('%Y-%m-%d - %H:%M:%S')}"

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