from datetime import datetime


class Account:
    accountCreationDate: datetime
    balance: float
    withdraws: list[tuple[datetime, float]]
    deposits: list[tuple[datetime, float]]
    operations: list[tuple[datetime, float]]
    withdrawCount: int

    def __init__(self):
        self.accountCreationDate = datetime.now()
        self.balance = 0
        self.withdraws = []
        self.deposits = []
        self.operations = []
        self.withdrawCount = 0

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        self.balance += amount
        self.deposits.append((datetime.now(), amount))


    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")

        if amount > 500:
            raise ValueError("Withdrawal amount exceeds limit of 500")

        if amount > self.balance:
            raise ValueError("Insufficient funds")

        if self.withdraws[-1][0].date() == datetime.now().date():
            if self.withdrawCount >= 3:
                raise ValueError("Withdrawal limit exceeded for today")
        else:
            self.withdrawCount = 0

        self.balance -= amount
        self.withdrawCount += 1
        self.withdraws.append((datetime.now(), amount * -1))

    def make_statement(self) -> str:
        operations = sorted(self.withdraws + self.deposits, key=lambda x: x[0])

        statement = f"Statement from {self.accountCreationDate.strftime('%m/%d/%Y')}\n"

        lastDate = None
        for date, amount in operations:
            if lastDate is None or date.date() != lastDate.date():
                statement += f"\n{date.strftime('%m/%d/%Y')}\n"
                lastDate = date

            amount = str(amount)
            statement += f"{date.time()} | {amount[0]}R${abs(float(amount)):.2f}\n"

        statement += f"\nBalance: R${self.balance:.2f}\n"
        return statement