from django.shortcuts import render
import time
import json
from django.http import JsonResponse,HttpResponse
from backend.blockchain.blockchain import BlockChain
from backend.blockchain.block import Block
from backend.pubsub import PubSub
from django.contrib.auth.decorators import login_required
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from django.views.decorators.csrf import csrf_exempt
from backend.wallet.transaction_pool import TransactionPool
from backend.products.assets import Assets
from backend.products.assets_transact import AssetsTransaction
from backend.products.assets_transpool import AssetsTransPool
from products.models import Products
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
block=BlockChain()
sender_assets=Assets(block)
wallet=Wallet(block)
assets=Assets(block)
transaction_pool=TransactionPool()
assetTranPool=AssetsTransPool()
pubsub=PubSub(block,transaction_pool,assetTranPool)
# Create your views here.
@login_required
def index(request):
    if assets.address!=request.user.username:
        assets.address=request.user.username
    return render(request,'index.html',{'Date':time.time()})
@login_required
def sell_transaction(request):
    if assets.address!=request.user.username:
        assets.address=request.user.username
    productID=int(request.GET.get('abc',None))
    if productID==None:
        return JsonResponse({'Error':'Error 204'},safe=False)
    Products.objects.filter(id=productID).update(ToBeSell=True)
    return index(request)
@login_required
def prevent_transaction(request):
    if assets.address!=request.user.username:
        assets.address=request.user.username
    productID=int(request.GET.get('abc',None))
    if productID==None:
        return JsonResponse({'Error':'Error 204'},safe=False)
    Products.objects.filter(id=productID).update(ToBeSell=False)
    return index(request)
@login_required
def buy_transaction(request):
    if assets.address!=request.user.username:
        assets.address=request.user.username
    productID=int(request.GET.get('abc',None))

    if productID==None:
        return JsonResponse({'Error':'Error 204'},safe=False)
    else:
        data = Products.objects.all().filter(id=productID)
        contex={}
        # try:
        p_id=list(data.values_list('id', flat=True))[0]
        p_owner_old=list(data.values_list('p_owner', flat=True))[0]
        user=User.objects.get(username=request.user.username)
        us_id=user.id
        sender_assets.address=User.objects.get(id=p_owner_old).username
        assetTran=assetTranPool.existing_transaction(sender_assets.address)
        if assetTran:
            assetTran.update(sender_assets,request.user.username,p_id)
        else:
            assetTran=AssetsTransaction(sender_assets,request.user.username,p_id)
            assetTranPool.set_transaction(assetTran)
   
        pubsub.broadcast_asset(assetTran)
        resp=blockMine(request)
        resp_data=json.loads(resp.content)
        is_mine_err='Error' in resp_data.keys()
        # return JsonResponse({'Done':'Error 204'},safe=False)
        if is_mine_err:
            return JsonResponse({'Error':'Error in Mining'},safe=False)
        #     print('Mined')
        #    
        #     update=  Products.objects.filter(id=p_id).update(p_owner=us_id)
        #     return JsonResponse(assetTran.to_json(),safe=False)
        else:
            contex={'id':p_id,'p_owner':p_owner_old,'p_owner_new':us_id,'sender_asset':User.objects.get(id=p_owner_old).username}
            update=  Products.objects.filter(id=p_id).update(p_owner=us_id)
            return JsonResponse({'Staus':'Mined'},safe=False)
        

@login_required
def blockChainRange(request):
    if assets.address!=request.user.username:
        assets.address=request.user.username
    start=int(request.GET.get('start',None))
    end=int(request.GET.get('end',None))
    # print(start,end)
    response=JsonResponse(block.to_json()[::-1][start:end],safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"

    return response
    # return JsonResponse({'start':start},safe=False)
@login_required
def blockChainLegth(request):
    if assets.address!=request.user.username:
        assets.address=request.user.username
    response=JsonResponse(len(block.chain),safe=False)
    # response["Access-Control-Allow-Origin"] = "*"
    # response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    # response["Access-Control-Max-Age"] = "1000"
    # response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response
@login_required
def blockchain(request):
    if assets.address!=request.user.username:
        assets.address=request.user.username
    return JsonResponse(block.to_json(),safe=False)
@login_required
def blockMine(request):
    if assets.address!=request.user.username:
        assets.address=request.user.username
    transaction_data=assetTranPool.transaction_data()
    print(transaction_data)
    if len(transaction_data)<1:
        contex={'Error':'Error'}
        return JsonResponse(contex,safe=False)

    # transaction_data.append(Transaction.reward_transaction(wallet).to_json())
    # transaction_data=assetTranPool.transaction_data()
    # print(transaction_data)
    block.addBlock(transaction_data)
    blck=block.chain[-1]
        # print(blck.to_json())
        # blck=Block(transaction_data)
    pubsub.broadcast_block(blck)
    assetTranPool.clear_blockchain_transactions(block)

    contex={'block_chain':block.chain[-1].to_json()}
    return JsonResponse(contex,safe=False)

    
@login_required
def walletInfo(request):
    if assets.address!=request.user.username:
        assets.address=request.user.username
    return JsonResponse({"address":wallet.address,"Balance":wallet.balance})
@login_required
def assetsInfo(request):
    if assets.address!=request.user.username:
        assets.address=request.user.username
    return JsonResponse({"address":assets.address,"Products":assets.products})
@login_required
def knwonaddresses(request):
    if assets.address!=request.user.username:
        assets.address=request.user.username
    known_addresses=set()
    for b in block.chain:
        for transaction in b.data:
            known_addresses.update(transaction['output'].keys())
    return JsonResponse(list(known_addresses),safe=False)
@login_required
def transactions(request):
    if assets.address!=request.user.username:
        assets.address=request.user.username
    return JsonResponse(assetTranPool.transaction_data(),safe=False)
@login_required
@csrf_exempt
def assetTransact(request):
    if assets.address!=request.user.username:
        assets.address=request.user.username
    if request.method == 'POST':
        transaction_data = json.loads(request.body.decode('utf-8'))
        print(transaction_data)
        assetTran=assetTranPool.existing_transaction(assets.address)
        if assetTran:
            assetTran.update(assets,transaction_data['recipient'],transaction_data['amount'])
        else:
            assetTran=AssetsTransaction(assets,transaction_data['recipient'],transaction_data['amount'])
        pubsub.broadcast_asset(assetTran)
        return JsonResponse(assetTran.to_json(),safe=False)
        # return JsonResponse({'ali1':'aa'},safe=False)
    if request.method== 'GET':
        return JsonResponse({'ali':'aa'},safe=False)
@login_required
@csrf_exempt
def walletTransact(request):
    if assets.address!=request.user.username:
        assets.address=request.user.username
    if request.method == 'POST':
        transaction_data = json.loads(request.body.decode('utf-8'))
        print(transaction_data)
        transaction=transaction_pool.existing_transaction(wallet.address)
        if transaction:
            transaction.update(wallet,transaction_data['recipient'],transaction_data['amount'])
        else:
            transaction=Transaction(wallet,transaction_data['recipient'],transaction_data['amount'])
        pubsub.broadcast_transaction(transaction)
        return JsonResponse( transaction.to_json(),safe=False)
        # return JsonResponse({'ali1':'aa'},safe=False)
    if request.method== 'GET':
        return JsonResponse({'ali':'aa'},safe=False)


        
