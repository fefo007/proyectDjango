from django.shortcuts import render,redirect
# from django.shortcuts import get_object_or_404
from .models import Order,Travel,Avatar,Messages,Tours
from .forms import UserEdit,SendMessage,OrderForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.models import User

def error_404(req,exception):
    return render(req,'404error.html')

def buy_travel(req,travelid):
    user = req.user
    travel = Travel.objects.get(id=travelid)
    if req.method == 'POST':
        form = OrderForm(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            order = Order(
                client = user,
                travel = travel.name,
                price = travel.price,
                wayToPay = data['wayToPay'],
                departure = data['departure'],
                arrival = data['arrival']
                )
            order.save()
            return redirect('orders')
    else:
        order_form = OrderForm()
        return render(req,'buy.html',{'travel':travel,'form':order_form})
    
def contact(req):
    if req.method == 'POST':
        message_form = SendMessage(req.POST)
        if message_form.is_valid():
            data = message_form.cleaned_data
            addressee = data['addressee']
            subject = data['subject']
            message = data['message']

            template = render_to_string('email_template.html',{
                'addressee' : addressee,
                'subject' : subject,
                'message' : message,
            })

            email = EmailMessage(
                subject,
                template,
                settings.EMAIL_HOST_USER,
                ['federicohfracaro@gmail.com']
            )

            email.fail_silently = False
            email.send()
            messages.success(req,'Email enviado con exito!')
            msg = Messages(
                client = req.user,
                addressee = data['addressee'],
                subject = data['subject'],
                message = data['message']
            )
            msg.save()
            return redirect('contact')
    else:
        message_form = SendMessage()
        return render(req,'contact.html',{'form':message_form})

def user_login(req):
    if req.user.is_authenticated:
        return redirect('home')
    else:
        if req.method == 'POST':
            user_form = AuthenticationForm(req,data=req.POST)
            if user_form.is_valid():
                data = user_form.cleaned_data
                username = data['username']
                password = data['password']
                user = authenticate(username=username,password=password)
                if user:
                    login(req,user)
                    return redirect('home')
                else:
                    user_form = AuthenticationForm(instance={'username':username})
                    return render(req,'login.html',{'msj':f'Usuario no registrado o password incorrecto',"user_form":user_form})
            else:
                user_form = AuthenticationForm()
                return render(req,'login.html',{'msj':f'Datos incorrectos',"user_form":user_form})
        else:
            user_form = AuthenticationForm()
            return render(req,'login.html',{"user_form":user_form})
    
def user_register(req):
    if req.method == 'POST':
        usercreate_form = UserCreationForm(req.POST)
        if usercreate_form.is_valid():
            usercreate_form.save()
            avatar = Avatar(
                user = User.objects.get(username = req.POST['username']),
                image = "avatares/userimg.png"
            )
            avatar.save()
            return render(req,'register.html',{"mensaje":f'usuario creado correctamente'})
        usercreate_form = UserCreationForm()
        return render(req,'register.html',{"msj":f'error al crear el usuario, intente denuevo',"form":usercreate_form})
    else:
        usercreate_form = UserCreationForm()
        return render(req,'register.html',{"form":usercreate_form})
    
@login_required
def user_edit(req):
    user = req.user
    avatar = Avatar.objects.get(user = req.user.id)
    # avatar = get_object_or_404(Avatar,user = req.user.id)
    if req.method == 'POST':
        useredit_form = UserEdit(req.POST,req.FILES,instance = {'avatar':avatar,'user':user})
        if useredit_form.is_valid():
            dataUser = useredit_form['user'].cleaned_data
            dataAvatar = useredit_form['avatar'].cleaned_data
            user.username = dataUser['username']
            user.first_name = dataUser['first_name']
            user.last_name = dataUser['last_name']
            user.email = dataUser['email']
            avatar.user = req.user
            avatar.image = dataAvatar['image']
            useredit_form.save()
            return redirect('home')
        return render(req,'error.html',{"mensaje":f'error al actualizar el usuario, intente denuevo'})
    else:
        useredit_form = UserEdit(instance = {'avatar':avatar,'user':user})
        return render(req,'user.html',{"form":useredit_form,'avatar_img':avatar.image.url})


@login_required  
def avatar_img(req):
    try:
        avatar = Avatar.objects.get(user = req.user.id)
        return render(req,'user.html',{'avatar_img':avatar.image.url})
    except:
        return render(req,'user.html')

def aboutUs(req):
    return render(req,'aboutUs.html')


class TravelListView(ListView):
    model = Travel
    template_name = 'travels.html'
    context_object_name = 'travels'

class TravelDetailView(DetailView):
    model = Travel
    template_name = 'travel_detail.html'
    context_object_name = 'travel'

class HomeView(ListView):
    model = Tours
    template_name = 'home.html'
    context_object_name = 'tours'

class OrdersView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'