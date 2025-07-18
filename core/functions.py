from datetime import datetime

from core.models import Withdrawal, Account


def can_make_withdrawal(account: Account) -> bool:
    withdrawals = Withdrawal.objects.filter(from_account=account)
    withdrawals_today = withdrawals.filter(timestamp__date=datetime.now().date()).count()

    if withdrawals_today >= 3:
        return False
    return True

def is_cpf_valid(cpf: str) -> bool:
    """
    Validate a Brazilian CPF (Cadastro de Pessoa Física) number.

    Parameters:
        cpf (str): A string of exactly 11 numeric digits (no dots or hyphens).

    Returns:
        bool: True if the CPF is valid, False otherwise.
    """
    # Must be 11 digits long and contain only numbers
    if not cpf.isdigit() or len(cpf) != 11:
        return False

    # Reject CPFs with all digits the same (e.g., "00000000000", "11111111111", etc.)
    if cpf == cpf[0] * 11:
        return False

    def calculate_digit(partial_cpf: str, weight_start: int) -> int:
        """
        Calculate one check digit for a CPF.

        Multiply each digit in partial_cpf by decreasing weights starting from weight_start,
        sum the results, compute sum % 11, and apply the CPF rule:
        if remainder < 2, digit = 0; otherwise digit = 11 - remainder.
        """
        total = 0
        weight = weight_start
        for ch in partial_cpf:
            total += int(ch) * weight
            weight -= 1
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder

    # Calculate first check digit (weights 10 down to 2)
    first_digit = calculate_digit(cpf[:9], 10)
    # Calculate second check digit (weights 11 down to 2, including the first check digit)
    second_digit = calculate_digit(cpf[:9] + str(first_digit), 11)

    # Compare with the last two digits of the CPF
    return cpf[-2:] == f"{first_digit}{second_digit}"


# def is_cpf_valid(cpf: str) -> bool:
#     if not cpf or len(cpf) != 11 or not cpf.isdigit():
#         return False
#
#     def calculate_digit(cpf, factor):
#         total = sum(int(digit) * factor for digit, factor in zip(cpf[:factor - 1], range(factor, 1, -1)))
#         remainder = total % 11
#         return '0' if remainder < 2 else str(11 - remainder)
#
#     first_digit = calculate_digit(cpf, 10)
#     second_digit = calculate_digit(cpf, 11)
#
#     return cpf[-2:] == first_digit + second_digit