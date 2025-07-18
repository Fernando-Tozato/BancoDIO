from django.urls import path

from core.views import make_deposit, make_withdrawal, make_transfer, get_statement, create_account, get_accounts, \
    get_account_details, create_client, get_client, activate_account, inactivate_account

urlpatterns = [
    path('deposit/', make_deposit, name='deposit'),
    path('withdrawal/', make_withdrawal, name='withdrawal'),
    path('transfer/', make_transfer, name='transfer'),
    path('statement/<str:account_number>/', get_statement, name='statement'),
    path('account/create/', create_account, name='account_create'),
    path('account/get/', get_accounts, name='account_get_all'),
    path('account/get/<str:client_cpf>/', get_accounts, name='account_get_client'),
    path('account/details/<str:account_number>/', get_account_details, name='account_get_detail'),
    path('account/activate/<str:account_number>/', activate_account, name='activate_account'),
    path('account/inactivate/<str:account_number>/', inactivate_account, name='inactivate_account'),

    path('client/create/', create_client, name='client_create'),
    path('client/get/<str:client_cpf>/', get_client, name='client_detail'),

]