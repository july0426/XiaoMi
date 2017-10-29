from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse,HttpResponseRedirect
from myadmin.models import Detail,Goods,Orders
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
import time
# 订单详情
def detailindex(request,pIndex):
	list1 = Detail.objects.filter()
	p = Paginator(list1, 7)
	if pIndex == '':
		pIndex = '1'
	list2 = p.page(pIndex)
	plist = p.page_range
	return render(request, 'myadmin/detail/index.html', {'list': list2, 'plist': plist, 'pIndex': pIndex})
def detailadd(request):
	return render(request,'myadmin/detail/add.html')
def detailinsert(request):
	try:
		ob=Detail()
		ob.orderid = request.POST['orderid']
		ob.goodsid = request.POST['goodsid']
		ob.name = request.POST['name']
		ob.price = request.POST['price']
		ob.num = request.POST['num']
		ob.save()
		context={'info':'添加成功'}
	except:
		context={'info':'添加失败'}
	return render(request,'myadmin/detail/info.html',context)
  
def detaildel(request,uid):
	try:
		ob = Detail.objects.get(id=uid)
		ob.delete()
		context = {'info':'删除成功！'}
	except:
		context = {'info':'删除失败！'}
	return render(request,"myadmin/detail/info.html",context)
def detailedit(request,uid):
	ob = Detail.objects.get(id = uid)
	context = {'detail':ob}
	return render(request,'myadmin/detail/edit.html',context)
def detailupdate(request,uid):
	print(request.POST)
	try:
		ob = Detail.objects.get(id= uid)
		ob.orderid = request.POST['orderid']
		ob.goodsid = request.POST['goodsid']
		ob.name = request.POST['name']
		ob.price = request.POST['price']
		ob.num = request.POST['num']
		ob.save()
		context = {'info':'修改成功！'}
	except:   
		context = {'info':'修改失败'}
	return render(request,"myadmin/detail/info.html",context)
# 订单表
def ordersindex(request,pIndex):
	list1 = Orders.objects.filter()
	
	print(list1)
	# detaillist = {}
	for ob in list1:
		id = ob.id
		ob.ob = Detail.objects.filter(orderid = id)
		
		# detaillist[id] = Detail.objects.filter(orderid = id)
		# print(detaillist[id])

	p = Paginator(list1, 7)
	if pIndex == '':
		pIndex = '1'
	list2 = p.page(pIndex)
	plist = p.page_range
	return render(request, 'myadmin/orders/index.html', {'list': list2, 'plist': plist, 'pIndex': pIndex})
def ordersadd(request):
	return render(request,'myadmin/orders/add.html')
def ordersinsert(request):
	# try:
		a=Orders()
		a.uid=request.POST["uid"]
		a.linkman=request.POST['linkman']
		a.address=request.POST['address']
		a.status=request.POST['status']
		a.code=request.POST['code']
		a.phone=request.POST['phone']
		a.total=request.POST['total']
		a.addtime=time.time()
		a.save()
		context={'info':'添加成功'}
	# except:
		# context={'info':'添加失败'}
		return render(request,'myadmin/orders/info.html',context)
  
def ordersdel(request,uid):
	try:
		ob = Orders.objects.get(id=uid)
		ob.delete()
		context = {'info':'删除成功！'}
	except:
		context = {'info':'删除失败！'}
	return render(request,"myadmin/orders/info.html",context)
def ordersedit(request,uid):
	ob = Orders.objects.get(id = uid)
	context = {'order':ob}
	return render(request,'myadmin/orders/edit.html',context)
def ordersupdate(request,uid):
	
	a = Orders.objects.get(id= uid)
	
	a.status=request.POST['status']
	
	a.save()
	
	context = {'info':'修改成功'}
	return render(request,"myadmin/orders/info.html",context)
