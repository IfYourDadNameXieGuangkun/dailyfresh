
from django.conf.urls import url
#from user import views
from user.views import RegisterView,ActiveView,LoginView
app_name = 'user'
urlpatterns = [

    #url(r'^register$',views.register,name='register'),#注册页面
    #url(r'^register_handle$',views.register_handle,name='register_handle')#用户点击注册
    url(r'^register$',RegisterView.as_view(),name='register'),
    url(r'^active/(?P<token>.*)$',ActiveView.as_view(),name='active'),
    url(r'^login$',LoginView.as_view(),name='login')
]
