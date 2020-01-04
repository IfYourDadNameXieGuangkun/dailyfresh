from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
app = Celery('celery_tasks.tasks',broker='192.168.19.60:6379/15')

@app.task
def send_register_active_email(to_email, username, token):
    username = username
    subject = '淘宝用户注册验证'
    # message = 'https://127.0.0.1:8000/user/active/'+token
    message = ''
    html_message = '<h1>%s,欢迎注册天天生鲜会员</h1>请点击下面的机会链接激活您的账户<br/><a herf="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
    username, token, token)
    print(message)
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    # 3.3发邮件
    send_mail(subject, message, sender, receiver, html_message=html_message)