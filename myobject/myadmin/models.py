from django.db import models

# Create your models here.

# 用户表
class Users(models.Model):
	username = models.CharField(max_length=32)
	name = models.CharField(max_length=16)
	passwd = models.CharField(max_length=32)
	sex = models.IntegerField(max_length=1)
	address = models.CharField(max_length=255)
	code = models.CharField(max_length=6)
	phone = models.CharField(max_length=16)
	email = models.CharField(max_length=50)
	state = models.IntegerField(max_length=1,default=1)
	addtime = models.IntegerField()
	class Meta:
		db_table = "myweb_users"
	def toDict(self):
		return {'name':self.name,'state':self.state,'username':self.username}

# 商品分类
class Type(models.Model):
	name = models.CharField(max_length=32)
	pid = models.IntegerField(default=0)
	path = models.CharField(max_length=255)
	class Meta:
		db_table = "myweb_type"
# 商品信息表
class Goods(models.Model):
	typeid = models.IntegerField()
	goods = models.CharField(max_length=32)
	company = models.CharField(max_length=50)
	descr = models.TextField()
	price = models.DecimalField(max_digits=6, decimal_places=2)
	picname = models.CharField(max_length=255)
	state = models.IntegerField(max_length=1,default=1)
	store = models.IntegerField(default=0)
	num = models.IntegerField(default=0)
	clicknum = models.IntegerField(default=0)
	addtime = models.IntegerField()
	class Meta:
		db_table = "myweb_goods"
	def toDict(self):
		return {'typeid':self.id,'goods':self.goods,'picname':self.picname,'price':self.price,'id':self.id,'m':1}
# 商品详情表
class Detail(models.Model):
	orderid = models.IntegerField()
	goodsid = models.IntegerField()
	name = models.CharField(max_length=32)
	price = models.DecimalField(max_digits=6, decimal_places=2)
	num = models.IntegerField()
	class Meta:
		db_table = "myweb_detail"
#商品订单表
class Orders(models.Model):
	uid = models.IntegerField()
	linkman = models.CharField(max_length=32)
	address = models.CharField(max_length=255)
	code = models.CharField(max_length=6)
	phone = models.CharField(max_length=16)
	addtime = models.IntegerField()
	total = models.DecimalField(max_digits=6, decimal_places=2)
	status = models.IntegerField()
	class Meta:
		db_table = "myweb_orders"
# 图片
class Pic(models.Model):
	name = models.CharField(max_length=32)
	age = models.IntegerField()
	picname = models.CharField(max_length=32)
	addtime = models.IntegerField()
	class Meta:
		db_table = "myweb_pic"


   