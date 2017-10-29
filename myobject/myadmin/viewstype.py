from django.shortcuts import render,redirect
from myadmin.models import Type,Goods
import time
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
 
from django.core.urlresolvers import reverse


#查看商品信息
def typeindex(request):
    # 执行数据查询，并放置到模板中
    list1 = Type.objects.extra(select = {'_has':'concat(path,id)'}).order_by('_has')
    # 遍历查询结果，为每个结果对象追加一个pname属性，目的用于缩进标题
    for ob in list1:
        ob.pname ='. . . '*(ob.path.count(',')-1)
    context = {"typelist":list1}
    return render(request,'myadmin/type/index.html',context)
#加载添加商品信息
def typeadd(request):
    return render(request,'myadmin/type/add.html')
def typeadds(request):
    dlist = Type.objects.filter()
    list = []
    for ob in dlist:
        list.append({'id':ob.id,'name':ob.name})
    return JsonResponse({'data':list})
#添加商品类别
def typeinsert(request):
    print(request.POST)
    ob = Type()
    ob.name = request.POST['name']
    pid = int(request.POST['id'])
    if pid == 0 :
        ob.pid = 0 
        ob.path = '0,'
        print(1)
    else:
        ob.pid = str(pid)
        path = Type.objects.get(id= pid)
        
        ob.path = path.path+str(pid)+','
    ob.save()
    context = {'info':'添加成功'}
    return render(request,'myadmin/type/info.html',context)
#删除商品
def typedel(request,uid):
    try:
        row = Type.objects.filter(pid=uid).count()
        if row > 0:
            context = {'info':'删除失败：此类别下还有子类别！'}
            return render(request,"myadmin/type/info.html",context)
        good = Goods.objects.filter(typeid=uid).count()
        if good > 0:
            context = {'info':'删除失败：此类别下还有商品！'}
            return render(request,"myadmin/type/info.html",context)
        ob = Type.objects.get(id=uid)
        ob.delete()
        context = {'info':'删除成功'}
    except:
        context = {'info':'删除失败'}
    return render(request,'myadmin/type/info.html',context)
#加载修改商品信息
def typeedit(request,uid):
    # try:
        ob = Type.objects.get(id=uid)
        p = ob.pid
        print(p)
        if p==0:
            context = {'type':ob,'pname':'根类别','pnid':0}
        else:
            pn = Type.objects.get(id=p)
            context = {'type':ob,'pname':pn.name,'pnid':pn.id}
        
        
        return render(request,'myadmin/type/edit.html',context)
    # except:
        # context = {'info':'没有要修改的信息'}
        # return render(request,'myadmin/type/info.html',context)
#修改商品信息
def typeedits(request):
    dlist = Type.objects.filter()
    list = []
    for ob in dlist:
        list.append({'id':ob.id,'name':ob.name})
    return JsonResponse({'data':list})
def typeupdate(request,uid):
    try:
        ob = Type.objects.get(id=uid)
        ob.name = request.POST['name']
        p = request.POST['id']
        ob.pid = p
        path = Type.objects.get(id= p)
        if path.path == '0,':
            ob.path = '0,'
        else:
            ob.path = path.path+str(p)+','
        ob.save()
        context = {'info':'修改成功'}
    except:
        context = {'info':'修改失败'}
    return render(request,'myadmin/type/info.html',context)
