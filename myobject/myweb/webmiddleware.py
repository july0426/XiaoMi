from django.shortcuts import redirect
from django.core.urlresolvers import reverse

import re
class WebMiddleware(object):
	def __init__(self,get_response):
		self.get_response = get_response
		
	def __call__(self, request):
		# 定义网站前台必须登录才能访问的路由url
		urllist=['/gwc','/gwcadd','/dingdan','/dingdans','/dingdancf','/logout','/admin','/personalupdate']
		#获取当前请求路径
		path=request.path
		# 判断当前请求是否是访问网站前台,并且path在urllist中
		if path  in urllist:
			#判断当前用户是否没有登陆
			if 'user' not in request.session:
				#执行登陆页面跳转
				return redirect(reverse('login'))
		response=self.get_response(request)
		return response