from account import Account
from console_user_interface import ConsoleUserInterface


class AppController:
    cui: ConsoleUserInterface
    account: Account

    def __init__(self):
        self.cui = ConsoleUserInterface()
        self.account = Account()

    def run(self):
        while True:
            option = self.cui.main_menu()

            match option:
                case 1:
                    amount = self.cui.deposit_menu()
                    try:
                        self.account.deposit(amount)
                        print("Deposit successful!")
                    except ValueError as e:
                        print(f"Error: {e}")

                case 2:
                    amount = self.cui.withdrawal_menu()
                    try:
                        self.account.withdrawal(amount)
                        print("Withdrawal successful!")
                    except ValueError as e:
                        print(f"Error: {e}")

                case 3:
                    statement = self.account.make_statement()
                    self.cui.statement_menu(statement)

                case 0:
                    self.cui.exit()