from django.conf.urls import url,include
from . import views,viewsusers
urlpatterns = [
   
   #注册
   url(r'^zhuce$', viewsusers.zhuce, name = "zhuce"),
   url(r'^zhucein$', viewsusers.zhucein, name = "zhucein"),
   #登录
   url(r'^login$', viewsusers.login,name = "login"),
   url(r'^verify$', viewsusers.verify, name="verify"), #验证码
    # url(r'^verifycodeValid/$', views.verifycodeValid),
   url(r'^logout$', viewsusers.logout,name = "logout"),
   url(r'^dologin$', viewsusers.dologin,name = "dologin"),
   # 网站前端商品展示
   # 会员及个人中心等路由配置
   url(r'^$', views.index, name = "index"),
   url(r'^/(?P<tid>[0-9]+)$', views.index, name = "index"),
   url(r'^list/(?P<tid>[0-9]+)$', views.list, name = "list"),
   url(r'^list$', views.list, name = "list"),
   url(r'^detail$', views.detail, name = "detail"),
   url(r'^detail/(?P<gid>[0-9]+)$', views.detail, name = "detail"),
   # 购物车及订单路由
   url(r'^gwc$', views.gwc, name = "gwc"),
   url(r'^gwcclear$', views.gwcclear, name = "gwcclear"),
   url(r'^gwcadd/(?P<gid>[0-9]+)$', views.gwcadd, name = "gwcadd"),
   url(r'^gwcdel/(?P<gid>[0-9]+)$', views.gwcdel, name = "gwcdel"),  
   url(r'^gwcchange$', views.gwcchange, name = "gwcchange"),
   url(r'^gwcchange1$', views.gwcchange1, name = "gwcchange1"),
   url(r'^dingdan$', views.dingdan, name = "dingdan"),
   url(r'^dingdancf$', views.dingdancf, name = "dingdancf"),
   url(r'^dingdans$', views.dingdans, name = "dingdans"),
   # 个人中心
   url(r'^admin$', viewsusers.admin, name = "admin"),
   url(r'^admins$', viewsusers.admins, name = "admins"),
   url(r'^adminid/(?P<gid>[0-9]+)$', viewsusers.adminid, name = "adminid"),

]