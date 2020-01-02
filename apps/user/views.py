from django.shortcuts import render,redirect
#from django.contrib.auth.models import User
from user.models import User
import re
from django.urls import reverse
from django.views import View

# Create your views here.

# /user/register
def register(request):
    '''显示注册页面'''
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        '''注册处理'''
        # 1.接受数据
        username = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 2.数据校验
        # 2.1参数判空
        if not all([username, pwd, cpwd, email]):
            return render(request, 'register.html', {'errormsg': '参数不完整'})

            # 2.2邮箱校验
        if not re.match(r'^[a-z0-9]+@[a-z0-9]+[\.]([a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errormsg': '邮箱不合法'})

            # 2.3是否同意规则
        if allow != 'on':
            return render(request, 'register.html', {'errormsg': '请同意协议'})

        # 3.业务处理,进行用户注册
        # 直接采用Django内置的用户认证系统

        # 3.1判断用户名是否已经存在:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:  # 不存在会报错 捕获异常
            user = None

        if user:
            return render(request, 'register.html', {'errormsg': '用户名已经存在'})
        user = User.objects.create_user(username, email, pwd)
        # 4.返回应答
        return redirect(reverse('goods:index'))

'''
此段逻辑融合到一个函数中 通过POST和GET区分请求处理逻辑
'''
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
    if not all([username,pwd,cpwd,email]):
        return render(request,'register.html',{'errormsg':'参数不完整'})

        #2.2邮箱校验
    if not re.match(r'^[a-z0-9]+@[a-z0-9]+[\.]([a-z]{2,5}){1,2}$',email):
        return render(request,'register.html',{'errormsg':'邮箱不合法'})

        #2.3是否同意规则
    if allow != 'on':
        return render(request,'register.html',{'errormsg':'请同意协议'})

    #3.业务处理,进行用户注册
        #直接采用Django内置的用户认证系统

        #3.1判断用户名是否已经存在:
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:#不存在会报错 捕获异常
        user = None

    if user:
        return render(request, 'register.html', {'errormsg': '用户名已经存在'})
    user = User.objects.create_user(username,email,pwd)
    #4.返回应答
    return redirect(reverse('goods:index'))



'''
使用类视图来代替函数视图 
'''

class RegisterView(View):

    def get(self , request):
        return render(request, 'register.html')

    def post(self , request):
        '''注册处理'''
        # 1.接受数据
        username = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        cpwd = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 2.数据校验
        # 2.1参数判空
        if not all([username, pwd, cpwd, email]):
            return render(request, 'register.html', {'errormsg': '参数不完整'})

            # 2.2邮箱校验
        if not re.match(r'^[a-z0-9]+@[a-z0-9]+[\.]([a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errormsg': '邮箱不合法'})

            # 2.3是否同意规则
        if allow != 'on':
            return render(request, 'register.html', {'errormsg': '请同意协议'})

        # 3.业务处理,进行用户注册
        # 直接采用Django内置的用户认证系统

        # 3.1判断用户名是否已经存在:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:  # 不存在会报错 捕获异常
            user = None

        if user:
            return render(request, 'register.html', {'errormsg': '用户名已经存在'})
        user = User.objects.create_user(username, email, pwd)
        # 4.返回应答
        return redirect(reverse('goods:index'))
