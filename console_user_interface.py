import os
import sys


class ConsoleUserInterface:
    def __init__(self):
        pass

    @staticmethod
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

    def main_menu(self) -> int:
        self.clear_console()

        text = '''
Welcome to the Bank System!

    1 - Make deposit
    2 - Make withdrawal
    3 - Get statement
    0 - Exit
                    '''
        possible_responses = list(range(0, 4))

        while True:
            print(text)
            response = input('Choose an option: ')

            if int(response) not in possible_responses:
                self.clear_console()
                print("Invalid option, please try again./n/n")
            else:
                return int(response)

    def deposit_menu(self) -> float:
        self.clear_console()
        text = '''
Please enter the amount you want to deposit (positive number): '''

        while True:
            amount = float(input(text))

            if amount <= 0:
                self.clear_console()
                print("Invalid amount. Please enter a positive number.")
            else:
                return amount



    def withdrawal_menu(self) -> float:
        self.clear_console()
        text = '''
Please enter the amount you want to withdrawal (positive number): '''

        while True:
            amount = float(input(text))

            if amount <= 0:
                self.clear_console()
                print("Invalid amount. Please enter a positive number.")
            else:
                return amount

    def statement_menu(self, statement: str):
        self.clear_console()
        print(statement)
        input("\n\nPress Enter to return to the main menu...")

    def exit(self):
        self.clear_console()
        print("Thank you for using the Bank System. Goodbye!")
        sys.exit()
