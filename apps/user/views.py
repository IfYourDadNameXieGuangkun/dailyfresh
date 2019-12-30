from django.shortcuts import render,redirect
from django.contrib.auth.models import User
import re
from django.urls import reverse
# Create your views here.

# /user/register
def register(request):
    '''显示注册页面'''
    return render(request,'register.html')

def register_handle(request):
    '''注册处理'''

    #1.接受数据
    username = request.POST.get('user_name')
    pwd = request.POST.get('pwd')
    cpwd = request.POST.get('cpwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')
    #2.数据校验
        #2.1参数判空
    # if not all([username,pwd,cpwd,email]):
    #     return render(request,'register.html',{'errormsg':'参数不完整'})
    #
    #     #2.2邮箱校验
    # if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+([a-z]{2,5}){1,2}$',email):
    #     return render(request,'register.html',{'errormsg':'邮箱不合法'})
    #
    #     #2.3是否同意规则
    # if allow != 'on':
    #     return render(request,'register.html',{'errormsg':'请同意协议'})

    #3.业务处理,进行用户注册
        #直接采用Django内置的用户认证系统
    #user = User.objects.create_user(username,email,pwd)
    #4.返回应答
    #return render(request,'login.html')
    return redirect(reverse('goods:index'))