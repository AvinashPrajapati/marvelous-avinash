import random,string
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from .models import CustomUser, Message, UserAvatar
from django.contrib import messages



def sendMail(msg, emailFrom, recipientList): 
    sub = 'welcome to Mysite world'
    send_mail( subject=sub, message='', from_email=emailFrom, recipient_list=recipientList, html_message=msg )
    print('send............')
def tokenGenerator():
    emptyToken = ''
    Token = emptyToken.join(random.choices(string.ascii_uppercase+string.digits, k = 8))
    return Token

# Create your views here.
def subscribe(request):
    user_avatar = UserAvatar.objects.all()
    random_avatar = random.choice(user_avatar)
    if request.method == "POST":
        try:
            email = request.POST['email']
            # print(email, '....................')
        except Exception as e:
            email = False
        try:
            name = request.POST['name']
            # print(name, '....................')
        except Exception as e:
            name = False
        try:
            avatar = request.FILES['avatar']
        except Exception as e:
            avatar = False

        if  (name=='' and email==''):
            messages.warning(request, 'Blanks fields are not allowed . . .')
            return redirect("chat:subscribe")
        token = tokenGenerator()

        email_exist = CustomUser.objects.filter(email = email)

        if not avatar:
            avatar = random_avatar.avatar
            print(avatar, '................')

        if email_exist:
            messages.warning(request, 'This email alread existed. if you unable to comment, please verify this email first.')
            return redirect("chat:subscribe")

        else:
            msg = f"<br>Hello,<b> {name}</b><br><br>Thank you for applying for subsription in marvelous-avinash.com .<br><br><p>your code: <b style='font-size:20px;'>{token}</b></p><br><span>Verification link: <a href=''> Verify -> </a></span><br><br><b>Regards ...</b><p>Marvelous-Avinash</p>"
            sender = settings.EMAIL_HOST_USER
            reciever = [email]
            newsletter = CustomUser(name=name, email=email, avatar=avatar, token=token)
            sendMail(msg, sender, reciever)
            # print("success..........")
            newsletter.save()
            messages.success(request, f'Mr. {email}, verification needed. Please enter the code sent to your mail.')
        return redirect("chat:verification")
    return render(request, 'chat/suscribe.html')

def verification(request):
    if request.method == "POST":
        token = request.POST['email']
        token = request.POST['token']
        try:
            tokenExist = CustomUser.objects.get(token = token)
        except Exception as e:
            messages.error(request,'Invalid Token.')
            return redirect("chat:verification")
        print(tokenExist.suscribed)

        if tokenExist.suscribed == 'suscribed':
            messages.warning(request,'Already verified.')
            return redirect("chat:verification")
        if tokenExist.suscribed == 'blocked':
            messages.error(request,'This email has been deleted. Try subscribe again then verify again ...')
            return redirect("chat:verification")
        if tokenExist and tokenExist.suscribed == 'unsuscribed':
            messages.success(request, f'Mr. {tokenExist.name},mail verified. Now, you can comment')
            tokenExist.suscribed = 'suscribed'
            tokenExist.save()
            return redirect("chat:verification")
    return render(request,'chat/suscrib-verify.html')

def resend_or_recover(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = CustomUser.objects.get(email = email)
            name = subscriber.name
            token = subscriber.token
            print(subscriber.token)
            message = f"<br>Hello,<b> {name}</b><br><br>Do not ' <i>forget it or share it with anyone </i>' .<br><br><p>your code: <b style='font-size:20px;'>{token}</b><p><br><b>Regards ...</b><p>Marvelous-Avinash</p>"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            messages.success(request, f'Mr. {name}, Check mail (Inbox or Spam section). ')
            sendMail(message, email_from, recipient_list)
            return redirect("chat:resend_or_recover")
        except Exception as e:
            messages.error(request,f"This '{email}' yet not registered.")
        return redirect("chat:resend_or_recover")
    return render(request,'chat/resend-or-recover.html')
