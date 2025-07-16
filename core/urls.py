from django.urls import path

from core.views import deposit, withdrawal, transfer, make_statement, account_detail, accounts

urlpatterns = [
    path('deposit/', deposit, name='deposit'),
    path('withdrawal/', withdrawal, name='withdrawal'),
    path('transfer/', transfer, name='transfer'),
    path('statement/<str:account_number>/', make_statement, name='statement'),
    path('accounts/', accounts, name='accounts'),
    path('account/<str:account_number>/', account_detail, name='account_detail'),
]