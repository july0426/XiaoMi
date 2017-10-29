from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse,HttpResponseRedirect
from myadmin.models import Users,Goods,Pic,Type,Detail,Orders
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
import time,os,shutil
from PIL import Image
def loadContext(request):
    context={}
    context['tlist'] = Type.objects.filter(pid=0)
    return context
def zhuce(request):
    return render(request,'myweb/zhuce.html')
def zhucein(request):
    verifycode = request.session['verifycode']
    code = request.POST['code1']
    print(request.POST)
    if verifycode != code:
        context = {'info':'验证码错误！'}
        return render(request,"myweb/zhuce.html",context)
    if request.POST['passwd'] != request.POST['passwd1']:
        context = {'info':'两次输入密码不正确！'}
        return render(request,"myweb/zhuce.html",context)  
    a = Users()
    a.username = request.POST['username']
    a.phone = request.POST['phone']
    import hashlib
    m=hashlib.md5()
    m.update(bytes(request.POST['passwd'],encoding='utf8'))
    a.passwd=m.hexdigest()  
    a.sex=request.POST['sex']
    a.name=request.POST['name']
    a.address=request.POST['address']
    a.code=request.POST['code']
    a.email=request.POST['email']
    a.state=1
    a.addtime=time.time()
    a.save()
    return render(request,'myweb/denglu.html')
def login(request):
    return render(request,'myweb/denglu.html')
def dologin(request):
    verifycode = request.session['verifycode']
    code = request.POST['code1']
    if verifycode != code:
        context = {'info':'验证码错误！'}
        return render(request,"myweb/denglu.html",context)
    try:
        user = Users.objects.get(username= request.POST['username'])
        # dict1 = user.__dict__
        # dict1.pop('_state')
        # print(dict1)
        if user.state != 2:
            # 验证密码
            import hashlib
            m=hashlib.md5()
            m.update(bytes(request.POST['passwd'],encoding='utf8'))
            if user.passwd==m.hexdigest():
                # dict1 = user.__dict__
                # request.session['user']={'id':user.id,'name':user.name,'username':user.username,'phone':user.phone}
                request.session['user']=user.toDict()
                print(request.session['user'])
                # request.session['user']=dict1
                # print(request.session['user'])
                return redirect(reverse('index'))
            else:
                context = {'info':'登录密码错误'}
        else:
            context = {'info':'此用户被禁用!'}
    except:
        context = {'info':'登录账号错误'}
    return render(request,'myweb/denglu.html',context)
def logout(request):
    # 清除登录的session信息
    del request.session['user']
    del request.session['shoplist']
    # 跳转登录页面(url地址改变)
    return redirect(reverse('index'))
# 会员登录表单
def verify(request):
    #引入随机函数模块
    import random
    from PIL import Image, ImageDraw, ImageFont
    #定义变量，用于画面的背景色、宽、高
    #bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242,164,247)
    width = 100
    height = 50
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = '1234567890'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/STXIHEI.TTF', 30)
    #font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 0), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 0), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 0), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 0), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
def login(request):
    return render(request,'myweb/denglu.html')
def admin(request):
    name = request.session['user']['name']
    users = Users.objects.get(name = name)
    context = loadContext(request)
    orderslists = Orders.objects.filter(uid = users.id)
    # print(orderslists)
    for order in orderslists:
        if order.status == 0:
            order.status = '已下单'
        elif order.status == 1:
            order.status = '已发货'
        elif order.status == 2:
            order.status = '已收货'
        else :
            order.status = '无效订单'
        id = order.id
        print(id)
        ob = Detail.objects.filter(orderid = id)
        order.ob = ob
        print(ob)
    context['user']=users
    context['orders']=orderslists
    print(request.POST)
    return render(request,'myweb/admin.html',context)
def admins(request):
    name = request.session['user']['name']
    users = Users.objects.get(name = name)
    # print(request.POST['address'])
    users.username = request.POST['username']
    users.address = request.POST['address']
    users.phone = request.POST['phone']
    users.code = request.POST['code']
    users.save()
    context = loadContext(request)
    orderslists = Orders.objects.filter(uid = users.id)
    # print(orderslists)
    for order in orderslists:
        if order.status == 0:
            order.status = '已下单'
        elif order.status == 1:
            order.status = '已发货'
        elif order.status == 2:
            order.status = '已收货'
        else :
            order.status = '无效订单'
        id = order.id
        print(id)
        ob = Detail.objects.filter(orderid = id)
        order.ob = ob
        print(ob)
    user = Users.objects.get(name = name)
    context['user']=user
    context['orders']=orderslists
    print(request.POST)
    return render(request,'myweb/adminss.html',context)
def adminid(request,gid):
    name = request.session['user']['name']
    users = Users.objects.get(name = name)
    context = loadContext(request)    
    orde = Orders.objects.get(id = gid)
    orde.status = 2
    orde.save()
    orderslists = Orders.objects.filter(uid = users.id)
    # print(orderslists)
    for order in orderslists:
        if order.status == 0:
            order.status = '已下单'
        elif order.status == 1:
            order.status = '已发货'
        elif order.status == 2:
            order.status = '已收货'
        else :
            order.status = '无效订单'
        id = order.id
        print(id)
        ob = Detail.objects.filter(orderid = id)
        order.ob = ob
        print(ob)
    context['user']=users
    context['orders']=orderslists
    print(request.POST)
    return render(request,'myweb/admin.html',context)