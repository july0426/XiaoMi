from myadmin.models import Goods,Type,Users,Detail,Orders
from django.shortcuts import render,redirect
import time
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse

def loadContext(request):
	context={}
	context['tlist'] = Type.objects.filter(pid=0)
	return context

# 首页
def index(request,tid=0):
    context = loadContext(request)
    # 获取所需商品列表信息并放置到context
    context['alllist'] = Goods.objects.order_by('num').filter(state__in=[1,2])[0:4]
    context['alllist1'] = Goods.objects.order_by('num').filter(state__in=[1,2])[5:9]
    context['zuixinlist'] = Goods.objects.order_by('addtime').filter(state__in=[1,2])[0:4]
    if tid == 0:
        context['stulist'] = Goods.objects.filter(state__in=[1,2])[0:12]
    else:
        #获取当前类别下的所有子类别信息
        context['Type'] = Type.objects.filter(pid=tid)
        # 判断参数ttid是否有值
        if request.GET.get('tid',None):
            tid = request.GET['tid']
            print(tid)
            context['stulist'] = Goods.objects.filter(typeid=tid).filter(state=2)[0:11]
            print(3)
            # print(context['stulist'])
        
        a = Type.objects.filter()
        
        pidlist = set()
        for i in a :
            pidlist.add(i.pid)
        print(pidlist)
        tid = int(tid)
        print(tid)
        if(tid in pidlist) :
            context['stulist'] = Goods.objects.filter(typeid__in=Type.objects.only('id').filter(path__contains=','+str(tid)+',')).filter(state=2)[0:11]
            
            print(2)
        else:
        # 获取指定商品类别下的所有商品信息
            context['stulist'] = Goods.objects.filter(typeid=tid).filter(state=2)[0:11]
            print(1)
    # 如tid=1的sql：select * from myweb_goods where typeid in(select id from myweb_type where path like '%,1,%')
    print(context)
    return render(request,'myweb/index.html',context)

# 列表页
def list(request,tid=0):
    context = loadContext(request)
    # 获取所需商品列表信息并放置到context
    if tid == 0:
        context['stulist'] = Goods.objects.filter(state=2)
    else:
        #获取当前类别下的所有子类别信息
        context['Type'] = Type.objects.filter(pid=tid)
        if request.GET.get('tid',None):
            tid = request.GET['tid']
            print(tid)
            context['stulist'] = Goods.objects.filter(typeid=tid).filter(state=2)[0:11]
            print(3)
            # print(context['stulist'])
        
        a = Type.objects.filter()
        
        pidlist = set()
        for i in a :
            pidlist.add(i.pid)
        print(pidlist)
        tid = int(tid)
        print(tid)
        if(tid in pidlist) :
            context['stulist'] = Goods.objects.filter(typeid__in=Type.objects.only('id').filter(path__contains=','+str(tid)+',')).filter(state=2)[0:11]
            
            print(2)
        else:
        # 获取指定商品类别下的所有商品信息
            context['stulist'] = Goods.objects.filter(typeid=tid).filter(state=2)[0:11]
            print(1)
    # 如tid=1的sql：select * from myweb_goods where typeid in(select id from myweb_type where path like '%,1,%')
    print(context)
    return render(request,'myweb/list.html',context)

# 商品详情
def detail(request,gid):
    context = loadContext(request)
    ob = Goods.objects.get(id=gid)
    ob.clicknum +=1
    ob.save()
    context['goods'] = ob
    return render(request,'myweb/detail.html',context)
def gwc(request):
	if 'shoplist' in request.session:
		pass
	else:
		request.session['shoplist']={}
	context = loadContext(request)
	return render(request,'myweb/gwc.html',context)
def gwcadd(request,gid):
	goods = Goods.objects.get(id = gid)
	shop = goods.toDict()
	shop['m'] = int(request.POST['m'])
	if 'shoplist' in request.session:
		shoplist = request.session['shoplist']
	else:
		shoplist = {}
	if gid in shoplist:
		shoplist[gid]['m']+=shop['m']
	else:
		shoplist[gid]=shop
	request.session['shoplist']=shoplist
	return redirect(reverse('gwc'))
def gwcclear(request):
	context = loadContext(request)
	request.session['shoplist'] = {}
	return render(request,"myweb/gwc.html",context)
def gwcdel(request,gid):
	shoplist = request.session['shoplist']
	del shoplist[gid]
	request.session['shoplist'] = shoplist
	return redirect(reverse('gwc'))
def gwcchange(request):
	context = loadContext(request)
	shoplist = request.session['shoplist']
	#获取信息
	shopid = request.GET['sid']
	num = int(request.GET['m'])
	store  = Goods.objects.get(id = shopid).store
	print(shopid)
	print(num)
	if num<1:
		num = 1
	else:
		if num >= store:
			context['info']='没有库存了哦,亲!'
			print(context['info'])
		else:
			num+=1

	shoplist[shopid]['m'] = num #更改商品数量
	request.session['shoplist'] = shoplist
	return render(request,"myweb/gwc.html",context)
def gwcchange1(request):
	context = loadContext(request)
	shoplist = request.session['shoplist']
	#获取信息
	shopid = request.GET['sid']
	num = int(request.GET['m'])
	print(shopid)
	print(num)
	if num<=1:
		num = 1
	else:
		num-=1
	shoplist[shopid]['m'] = num #更改商品数量
	request.session['shoplist'] = shoplist
	return render(request,"myweb/gwc.html",context)
def dingdan(request):
	if 'id' not in request.POST:
		return HttpResponse('选商品啊大哥!')
	total = 0	
	print(request.POST)
	val = request.POST.getlist('id')
	print(val)
	goodslist = {}
	shoplist = request.session['shoplist']
	for id in val:
	# 计算总金额
		total += shoplist[id]['price']*shoplist[id]['m'] 
		#累计总金额
			# 获取选购的商品信息
		ob = Goods.objects.get(id = id)
		ob.m = shoplist[id]['m'] 
		goodslist[id]=ob
	print(goodslist)	
	# print(val)	
	# print(shoplist)	
	print(ob.m)
	name = request.session['user']['name']
	users = Users.objects.get(name= name)
	context = loadContext(request)
	context['users']=users
	context['goodslist']=goodslist
	request.session['shoplist'] = shoplist
	context['total']=total
	# print(context)
	return render(request,"myweb/dingdan.html",context)
def dingdancf(request):
	if request.POST['linkman']=='':
		return HttpResponse('写联系人!!')
	if request.POST['phone']=='':
		return HttpResponse('写电话!!')
	if request.POST['code']=='':
		return HttpResponse('写邮编!')
	if request.POST['address']=='':
		return HttpResponse('写地址!')
	user = {}
	user['linkman'] = request.POST['linkman']
	user['address'] = request.POST['address']
	user['code'] = request.POST['code']
	user['phone'] = request.POST['phone']
	context = loadContext(request)
	context['user']=user
	total = 0	
	val = request.POST.getlist('sid')
	print(val)
	goodslist = {}
	shoplist = request.session['shoplist']
	for id in val:
	# 计算总金额
		total += shoplist[id]['price']*shoplist[id]['m'] 
		#累计总金额
			# 获取选购的商品信息
		ob = Goods.objects.get(id = id)
		ob.m = shoplist[id]['m']
		ob.save() 
		print(ob)
		goodslist[id]=ob
	print(goodslist)
	request.session['shoplist'] = shoplist
	context['goodslist']=goodslist
	context['total']=total
	return render(request,"myweb/dingdancf.html",context)
def dingdans(request):
	# user = Users.objects.get(name= request.session['name'])
	# print(request.session['shoplist'])
	shoplist = request.session['shoplist']
	print(shoplist)
	val = request.POST.getlist('sid')
	print(val)
	# 处理用户信息
	user = Users.objects.get(name = request.session['user']['name'])
	user.address = request.POST['address']
	user.code = request.POST['code']
	user.phone = request.POST['phone']
	user.save()
	total = 0
	for id in val:
		total += shoplist[id]['price']*shoplist[id]['m']
		# 处理订单信息
	order = Orders()
	order.uid = user.id
	order.linkman = request.POST['linkman']
	order.address = request.POST['address']
	order.code = request.POST['code']
	order.phone = request.POST['phone']
	order.addtime = time.time()
	order.total = total
	order.status = 0
	order.save()

	# 处理商品信息
	
	for id in val:
		detail = Detail()
		detail.orderid = order.id
		detail.goodsid = id
		detail.price = shoplist[id]['price']
		detail.name = shoplist[id]['goods']
		detail.num = shoplist[id]['m']
		detail.save()
		m = shoplist[id]['m']
		good = Goods.objects.get(id = id)
		good.num += shoplist[id]['m']
		good.store -= shoplist[id]['m']
		good.save()
		del shoplist[id] 
		print(m)
		print(good.num)
		print(good.store)
		

	request.session['shoplist'] = shoplist
	context = loadContext(request)
	context['info'] = "订单确认成功!"
	return render(request,"myweb/info.html",context)