from django.shortcuts import render,redirect
from myadmin.models import Goods,Type
import time
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
 
from django.core.urlresolvers import reverse
import time,os,shutil,json
from PIL import Image

#查看商品信息
def goodsindex(request,pIndex):
    # 执行数据查询，并放置到模板中
    list1 = Goods.objects.all()
    for i in list1:
        a = i.typeid
        b = Type.objects.get(id = a)
        i.type = b.name
    p = Paginator(list1,7)
    if pIndex=="":
        pIndex = '1'
    pIndex = int(pIndex)
    list2 = p.page(pIndex)
    plist = p.page_range
    # context = {"goodslist":list}
    return render(request,'myadmin/goods/index.html',{'goodslist':list2,'pIndex':pIndex,'plist':plist})
#加载添加商品信息
def goodsadd(request):
    return render(request,'myadmin/goods/add.html')
def goodsadds(request,pid):
    dlist = Type.objects.filter(pid=pid)
    list = []
    for ob in dlist:
        list.append({'id':ob.id,'name':ob.name})
    return JsonResponse({'data':list})
def goodsaddss(request):
    myfile = request.FILES.get("pic", None)
    if not myfile:
        return HttpResponse("没有上传文件信息！")
    # 以时间戳命名一个新图片名称
    filename= str(time.time())+"."+myfile.name.split('.').pop()
    destination = open(os.path.join("./static/goods/",filename),'wb+')
    for chunk in myfile.chunks():      # 分块写入文件  
        destination.write(chunk)  
    destination.close()
    return JsonResponse({'src':"./static/goods/"+filename})
#添加商品
def goodsinsert(request):
    try:
        # 判断并执行图片上传，缩放等处理
        myfile = request.FILES.get("pic", None)
        if not myfile:
            return HttpResponse("没有上传文件信息！")
        # 以时间戳命名一个新图片名称
       
        filename= str(time.time())+"."+myfile.name.split('.').pop()
        destination = open(os.path.join("./static/goods/",filename),'wb+')
        for chunk in myfile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()

        # 执行图片缩放
        im = Image.open("./static/goods/"+filename)
        # 缩放到375*375:
        im.thumbnail((375, 375))
        # 把缩放后的图像用jpeg格式保存:
        im.save("./static/goods/"+filename, 'jpeg')
        # 缩放到220*220:
        im.thumbnail((220, 220))
        # 把缩放后的图像用jpeg格式保存:
        im.save("./static/goods/m_"+filename, 'jpeg')
        # 缩放到220*220:
        im.thumbnail((100, 100))
    # 把缩放后的图像用jpeg格式保存:
        im.save("./static/goods/s_"+filename, 'jpeg')
        ob = Goods()
        ob.typeid = int(request.POST['typeid'])
        ob.goods = request.POST['goods']
        ob.company = request.POST['company']
        ob.descr = request.POST['descr']
        ob.price = request.POST['price']
        ob.picname = filename
        ob.state = request.POST['state']
        ob.store = request.POST['store']
        ob.num = 0
        ob.clicknum = 0
        ob.addtime = time.time()
        ob.save()
        print(ob)
        context = {'info':'添加成功'}
    except:
        context = {'info':'添加失败'}
    return render(request,'myadmin/goods/info.html',context)
#删除商品
def goodsdel(request,uid):
    try:
        ob = Goods.objects.get(id=uid)
        ob.delete()
        context = {'info':'删除成功'}
    except:
        context = {'info':'删除失败'}
    return render(request,'myadmin/goods/info.html',context)
#加载修改商品信息
def goodsedit(request,uid):
    try:
        ob = Goods.objects.get(id=uid)
        context = {'goods':ob}
        return render(request,'myadmin/goods/edit.html',context)
    except:
        context = {'info':'没有要修改的信息'}
        return render(request,'myadmin/goods/info.html',context)
#修改商品信息
def goodsupdate(request,uid):
    try:
        b = False
        oldpicname = request.POST['oldpicname']
        if None != request.FILES.get("pic"):
            myfile = request.FILES.get("pic", None)
            if not myfile:
                return HttpResponse("没有上传文件信息！")
            # 以时间戳命名一个新图片名称
            filename= str(time.time())+"."+myfile.name.split('.').pop()
            destination = open(os.path.join("./static/goods/",filename),'wb+')
            for chunk in myfile.chunks():      # 分块写入文件  
                destination.write(chunk)  
            destination.close()
            # 执行图片缩放
            im = Image.open("./static/goods/"+filename)
            # 缩放到375*375:
            im.thumbnail((375, 375))
            # 把缩放后的图像用jpeg格式保存:
            im.save("./static/goods/"+filename, 'jpeg')
            # 缩放到220*220:
            im.thumbnail((220, 220))
            # 把缩放后的图像用jpeg格式保存:
            im.save("./static/goods/m_"+filename, 'jpeg')
            # 缩放到220*220:
            im.thumbnail((100, 100))
        # 把缩放后的图像用jpeg格式保存:
            im.save("./static/goods/s_"+filename, 'jpeg')
            b = True
            picname = filename
        else:
            picname = oldpicname
        ob = Goods.objects.get(id=uid)
        ob.goods = request.POST['goods']
        ob.company = request.POST['company']
        ob.descr = request.POST['descr']
        ob.price = request.POST['price']
        ob.picname = picname
        ob.state = request.POST['state']
        ob.store = request.POST['store']
        ob.save()
        context = {'info':'修改成功'}
        if b:
            os.remove("./static/goods/m_"+oldpicname) #执行老图片删除  
            os.remove("./static/goods/s_"+oldpicname) #执行老图片删除  
            os.remove("./static/goods/"+oldpicname) #执行老图片删除  
    except:
        context = {'info':'修改失败'}
        if b:
            os.remove("./static/goods/m_"+picname) #执行新图片删除  
            os.remove("./static/goods/s_"+picname) #执行新图片删除  
            os.remove("./static/goods/"+picname) #执行新图片删除  
    return render(request,'myadmin/goods/info.html',context)
