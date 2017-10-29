from django.conf.urls import url,include
from . import views,viewsgoods,viewstype,viewsorders 
urlpatterns = [
# 后台首页
    url(r'^$', views.index,name = "myadmin_index"),
    # 后台管理员路由
    url(r'^login$', views.login,name = "myadmin_login"),
    url(r'^verify$', views.verify, name="verify"), #验证码
    # url(r'^verifycodeValid/$', views.verifycodeValid),
    url(r'^logout$', views.logout,name = "myadmin_logout"),
    url(r'^dologin$', views.dologin,name = "myadmin_dologin"),
    # 后台管理
    url(r'^users(?P<pIndex>[0-9]*)/$', views.usersindex,name = "myadmin_usersindex"),
    url(r'^usersadd$', views.usersadd,name = "myadmin_usersadd"),
    url(r'^usersinsert$', views.usersinsert,name = "myadmin_usersinsert"),
    url(r'^usersdel/(?P<uid>[0-9]+)$', views.usersdel,name = "myadmin_usersdel"),
    url(r'^usersedit/(?P<uid>[0-9]+)$', views.usersedit,name = "myadmin_userseidt"),
    url(r'^usersupdate/(?P<uid>[0-9]+)$', views.usersupdate,name = "myadmin_usersupdate"),
    # 后台商品管理
    url(r'^goods(?P<pIndex>[0-9]*)/$', viewsgoods.goodsindex,name = "myadmin_goodsindex"),
    url(r'^goodsadd$', viewsgoods.goodsadd,name = "myadmin_goodsadd"),
    url(r'^goodsadds/(?P<pid>[0-9]+)$', viewsgoods.goodsadds,name = "myadmin_goodsadds"),
    url(r'^goodsaddss$', viewsgoods.goodsaddss,name = "myadmin_goodsaddss"),
    url(r'^goodsinsert$', viewsgoods.goodsinsert,name = "myadmin_goodsinsert"),
    url(r'^goodsdel/(?P<uid>[0-9]+)$', viewsgoods.goodsdel,name = "myadmin_goodsdel"),
    url(r'^goodsedit/(?P<uid>[0-9]+)$', viewsgoods.goodsedit,name = "myadmin_goodseidt"),
    url(r'^goodsupdate/(?P<uid>[0-9]+)$', viewsgoods.goodsupdate,name = "myadmin_goodsupdate"),
    # 商品类别管理
    url(r'^type$', viewstype.typeindex,name = "myadmin_typeindex"),
    url(r'^typeadd$', viewstype.typeadd,name = "myadmin_typeadd"),
    url(r'^typeadds$', viewstype.typeadds,name = "myadmin_typeadds"),
    url(r'^typeinsert$', viewstype.typeinsert,name = "myadmin_typeinsert"),
    url(r'^typedel/(?P<uid>[0-9]+)$', viewstype.typedel,name = "myadmin_typedel"),
    url(r'^typeedit/(?P<uid>[0-9]+)$', viewstype.typeedit,name = "myadmin_typeeidt"),
    url(r'^typeedits$', viewstype.typeedits,name = "myadmin_typeedits"),
    url(r'^typeupdate/(?P<uid>[0-9]+)$', viewstype.typeupdate,name = "myadmin_typeupdate"),
    # 订单表
    url(r'^orders(?P<pIndex>[0-9]*)/$', viewsorders.ordersindex,name = "myadmin_ordersindex"),
    url(r'^ordersadd$', viewsorders.ordersadd,name = "myadmin_ordersadd"),
    url(r'^ordersinsert$', viewsorders.ordersinsert,name = "myadmin_ordersinsert"),
    url(r'^ordersdel/(?P<uid>[0-9]+)$', viewsorders.ordersdel,name = "myadmin_ordersdel"),
    url(r'^ordersedit/(?P<uid>[0-9]+)$', viewsorders.ordersedit,name = "myadmin_orderseidt"),
    url(r'^ordersupdate/(?P<uid>[0-9]+)$', viewsorders.ordersupdate,name = "myadmin_ordersupdate"),
    # 订单详情表
    url(r'^detail(?P<pIndex>[0-9]*)/$', viewsorders.detailindex,name = "myadmin_detailindex"),
    url(r'^detailadd$', viewsorders.detailadd,name = "myadmin_detailadd"),
    url(r'^detailinsert$', viewsorders.detailinsert,name = "myadmin_detailinsert"),
    url(r'^detaildel/(?P<uid>[0-9]+)$', viewsorders.detaildel,name = "myadmin_detaildel"),
    url(r'^detailedit/(?P<uid>[0-9]+)$', viewsorders.detailedit,name = "myadmin_detaileidt"),
    url(r'^detailupdate/(?P<uid>[0-9]+)$', viewsorders.detailupdate,name = "myadmin_detailupdate"),
    # 图片上传
    url(r'^pic$', views.indexpic, name="myadmin_pic"), #浏览相册图片信息
    url(r'^pic/add$', views.addpic, name="myadmin_addpic"), #加载添加相册图片信息表单
    url(r'^pic/insert$', views.insertpic, name="myadmin_insertpic"), #执行相册图片信息添加
    url(r'^pic/(?P<uid>[0-9]+)/del$', views.delpic, name="myadmin_delpic"), #执行相册图片信息删除
    url(r'^pic/(?P<uid>[0-9]+)/edit$', views.editpic, name="myadmin_editpic"), #加载相册图片信息编辑表单
    url(r'^pic/update$', views.updatepic, name="myadmin_updatepic"), #执行相册图片信息编辑
    url(r'^showpic$', views.showpic, name="myadmin_showpic"), #执行相册图片信息编辑
]