from account import Account
import os


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


class ConsoleUserInterface:
    def __init__(self):
        pass

    def loop(self, text: str, possible_responses: list[int]) -> int:
        while True:
            print(text)
            response = int(input('Choose an option: '))

            if response in possible_responses:
                return response
            else:
                clear_console()
                print("Invalid option, please try again./n/n")

    def main_menu(self) -> int:
        clear_console()
        text = '''
Welcome to the Bank System!

    1 - Make deposit
    2 - Make withdrawal
    3 - Get statement
    4 - Exit
                    '''
        possible_responses = list(range(1, 5))

        return self.loop(text, possible_responses)

    def deposit_menu(self):
        pass

    def withdrawal_menu(self):
        pass

    def statement_menu(self):
        pass

    def exit(self):
        pass
