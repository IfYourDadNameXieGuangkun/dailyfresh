from django.shortcuts import render,redirect
#from django.contrib.auth.models import User
from user.models import User
import re
from django.urls import reverse
from django.views import View
from itsdangerous import TimedJSONWebSignatureSerializer as Sign ,SignatureExpired
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from celery_tasks.tasks import send_register_active_email
from django.contrib.auth import authenticate,login
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
用户注册
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
        user.is_active = 0
        user.save()

        #3.2加密用户名
        username = user.username
        info = {'conform':user.id}
        sign = Sign(settings.SECRET_KEY , 3600)
        username_sign = sign.dumps(info)
        username_sign = username_sign.decode()
        subject = '淘宝用户注册验证'
        message = ''
        html_message = '<h1>%s,欢迎注册天天生鲜会员</h1>请点击下面的机会链接激活您的账户<br/><a herf="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>'%(username,username_sign,username_sign)
        # print(message)
        sender = settings.EMAIL_FROM
        receiver = [email]
        # #3.3发邮件
        send_mail(subject,message,sender,receiver,html_message=html_message)
        #send_register_active_email.delay(email,username,username_sign)
        # 4.返回应答
        return redirect(reverse('goods:index'))

'''
用户激活
'''
class ActiveView(View):
    def get(self,request,token):
        '''
        用户激活
        :param request:
        :return:
        '''
        #print('token:%s'%token)
        try:
            sign = Sign(settings.SECRET_KEY, 3600)
            info = sign.loads(token)
            user_id = info['conform']
            user = User.objects.get(id=user_id)
            print('user:' + user.username)
            user.is_active = 1
            user.save()
            #return HttpResponse('用户激活成功')
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse('链接已过期')


'''
用户登陆
get:登陆界面
post:登陆行为
'''
class LoginView(View):

    def get(self,request):
        #判断是否记住用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
            return render(request, 'login.html',{'username':username,'checked':checked})
        else:
            return render(request,'login.html')

    def post(self,request):
        password = request.POST.get('password')
        username = request.POST.get('username')
        remember = request.POST.get('remember')
        print('pswd:%s'%password)
        try:
            #user = User.objects.get(username = username)
            user = authenticate(username=username,password=password)

            login(request,user)
        except User.DoesNotExist:  # 不存在会报错 捕获异常
            user = None
            return render(request,'login.html',{'errormsg':'用户不存在'})
        if user:
            print('登录成功')
            if user.is_active:
                response = redirect(reverse('goods:index'))
                if remember=='on':
                    response.set_cookie('username',username,max_age=7*24*3600)
                else:
                    response.delete_cookie('username')
                return response
            else:
                print('未激活')
                return render(request, 'login.html', {'errormsg': '请在邮件中查收激活地址并进行激活'})
        else:
            print('用户不存在')
            return render(request, 'login.html', {'errormsg': '用户不存在'})
