from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('blockchain/',views.blockchain,name='printchain'),
    path('mineBlock/',views.blockMine,name='mineblock'),
     path('range/',views.blockChainRange),
     path('length/',views.blockChainLegth),
    path('wal_info/',views.walletInfo),
    path('wal_tran/',views.walletTransact),
    path('knownaddr/',views.knwonaddresses),
    path('transactions/',views.transactions),
    path('assetsInfo/',views.assetsInfo,name='assetinfo'),
      path('assetTrans/',views.assetTransact),
       path('buy/',views.buy_transaction),
        path('sell/',views.sell_transaction),
         path('prevent/',views.prevent_transaction)

]