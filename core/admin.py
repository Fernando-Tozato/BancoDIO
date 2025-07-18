from django.contrib import admin

from core.models import Operation, Deposit, Withdrawal, Transfer, Account, Client

admin.site.register(Client)
admin.site.register(Account)
admin.site.register(Operation)
admin.site.register(Deposit)
admin.site.register(Withdrawal)
admin.site.register(Transfer)