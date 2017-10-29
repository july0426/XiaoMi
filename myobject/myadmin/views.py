from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse,HttpResponseRedirect
from myadmin.models import Users,Goods,Pic
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
import time,os,shutil
from PIL import Image
def index(request):
	return render(request,'myadmin/index.html')
# 后台管理会员
# ============后台管理员操作================================
# 会员登录表单
def login(request):
	return render(request,'myadmin/login.html')
def dologin(request):
	verifycode = request.session['verifycode']
	code = request.POST['code']
	if verifycode != code:
		context = {'info':'验证码错误！'}
		return render(request,"myadmin/login.html",context)
	try:
		user = Users.objects.get(username= request.POST['username'])
		if user.state == 0:
			# 验证密码
			import hashlib
			m=hashlib.md5()
			m.update(bytes(request.POST['passwd'],encoding='utf8'))
			if user.passwd==m.hexdigest():
			# if user.passwd == request.POST['passwd']:
				request.session['adminuser'] = user.name
				return redirect(reverse('myadmin_index'))
			else:
				context = {'info':'登录密码错误'}
		else:
			context = {'info':'此用户非后台管理用户!'}
	except:
		context = {'info':'登录账号错误'}
	return render(request,'myadmin/login.html',context)
def logout(request):
	# 清除登录的session信息
	del request.session['adminuser']
	# 跳转登录页面(url地址改变)
	return redirect(reverse('myadmin_login'))
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
    height = 25
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
    font = ImageFont.truetype('static/STXIHEI.TTF', 21)
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

# 浏览会员信息
def usersindex(request,pIndex):
	list1 = Users.objects.filter()
	print(list1)
	for i in list1:
		if i.sex == 1:
			i.sex = '男'
		else:
			i.sex = '女'
	for x in list1:
		if x.state == 1:
			x.state = '启用'
		elif x.state == 0:
			x.state = '后台管理员'
		else:
			x.state = '禁用'		
	p = Paginator(list1, 7)
	if pIndex == '':
		pIndex = '1'
	list2 = p.page(pIndex)
	plist = p.page_range
	return render(request, 'myadmin/users/index.html', {'list': list2, 'plist': plist, 'pIndex': pIndex})
def usersadd(request):
	return render(request,'myadmin/users/add.html')
def usersinsert(request):
	try:
		a=Users()
		a.username=request.POST["username"]
		a.name=request.POST['name']
		import hashlib
		m=hashlib.md5()
		m.update(bytes(request.POST['passwd'],encoding='utf8'))
		a.passwd=m.hexdigest()
		a.sex=request.POST['sex']
		a.address=request.POST['address']
		a.code=request.POST['code']
		a.phone=request.POST['phone']
		a.email=request.POST['email']
		a.state=request.POST['state']
		a.addtime=time.time()
		a.save()
		context={'info':'添加成功'}
	except:
		context={'info':'添加失败'}
	return render(request,'myadmin/users/info.html',context)
  
def usersdel(request,uid):
	try:
		ob = Users.objects.get(id=uid)
		ob.delete()
		context = {'info':'删除成功！'}
	except:
		context = {'info':'删除失败！'}
	return render(request,"myadmin/users/info.html",context)
def usersedit(request,uid):
	ob = Users.objects.get(id = uid)
	context = {'user':ob}
	return render(request,'myadmin/users/edit.html',context)
def usersupdate(request,uid):
	try:
		ob = Users.objects.get(id= uid)
		ob.usersname = request.POST['usersname']
		ob.name = request.POST['name']
		ob.code = request.POST['code']
		ob.phone = request.POST['phone']
		ob.email = request.POST['email']
		ob.state = request.POST['state']
		ob.address = request.POST['address']
		ob.sex = request.POST['sex']
		ob.addtime = time.time()
		ob.save()
		context = {'info':'修改成功！'}
	except:   
		context = {'info':'修改失败'}
	return render(request,"myadmin/users/info.html",context)
# 图片上传
# 浏览相册图片信息信息        
def indexpic(request):
	# 执行数据查询，并放置到模板中
	list = Pic.objects.all()
	context = {"stulist":list}
	return render(request,"myadmin/pic/index.html",context)

# 加载添加信息表单
def addpic(request):  
	return render(request,"myadmin/pic/add.html")
# 执行信息添加操作
def insertpic(request): 
	# try:
		#执行图片的上传
		myfile = request.FILES.get("mypic", None)
		print(myfile)
		if not myfile:
			return HttpResponse("没有上传文件信息！")
		destination = open(os.path.join("./static/pic/",myfile.name),'wb+')
		for chunk in myfile.chunks():      # 分块写入文件  
			destination.write(chunk)  
		destination.close()
		class Graphics:
			infile=os.path.join("./static/pic/",myfile.name)
			outfile =os.path.join("./static/pic1/",myfile.name)
			@classmethod
			def fixed_size(cls, width, height):
				im = Image.open(cls.infile)
				out = im.resize((width, height),Image.ANTIALIAS)
				out.save(cls.outfile)
		fix = Graphics()
		fix.infile = './static/pic'+myfile.name 
		fix.outfile = './static/pic1'+myfile.name 
		Graphics.fixed_size(50,50)
		#执行信息的添加
		ob = Pic()
		ob.name = request.POST['name']
		ob.age = request.POST['age']
		ob.picname = myfile.name
		ob.addtime= time.time()
		ob.save()
		context = {'info':'添加成功！'}
	# except:
		# context = {'info':'添加失败！'}
		return render(request,"myadmin/users/info.html",context)
# 执行信息删除操作    
def delpic(request,uid):  
	try:
		ob = Pic.objects.get(id=uid)
		fileinfo = ob.picname #获取要删除的文件
		os.remove("./static/pic/"+fileinfo) #执行图片文件删除
		ob.delete()
		context = {'info':'删除成功！'}
	except:
		context = {'info':'删除失败！'}
	return render(request,"myadmin/users/info.html",context)
# 加载信息编辑表单    
def editpic(request,uid):  
	try:
		ob = Pic.objects.get(id=uid)
		context = {'pic':ob}
		return render(request,"myadmin/pic/edit.html",context)
	except:
		context = {'info':'没有找到要修改的信息！'}
		return render(request,"myadmin/users/info.html",context)
# 执行信息编辑操作
def updatepic(request):
	b = False
	oldpicname = request.POST['oldpicname']
	if None != request.FILES.get("mypic"):
		myfile = request.FILES.get("mypic", None)
		if not myfile:
			return HttpResponse("没有上传文件信息！")
		destination = open(os.path.join("./static/pic/",myfile.name),'wb+')
		for chunk in myfile.chunks():      # 分块写入文件  
			destination.write(chunk)  
			destination.close()
			picname = myfile.name
			b = True
	else:
		picname = oldpicname
	try:
		#判断是否有文件上传
		ob = Pic.objects.get(id= request.POST['id'])
		ob.name = request.POST['name']
		ob.age = request.POST['age']
		ob.picname = picname
		ob.save()
		context = {'info':'修改成功！'}
		if b:
			os.remove("./static/pic/"+oldpicname) #执行老图片删除  
	except:
		context = {'info':'修改失败！'}
		if b:
			os.remove("./static/pic/"+picname) #执行新图片删除  
	return render(request,"myadmin/users/info.html",context)
def showpic(request):
	a = Pic.objects.filter()
	context = {'list':a}
	return render(request,"myadmin/pic/showpic.html",context)	

	