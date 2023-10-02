from django.shortcuts import render,redirect
from django.http import HttpResponse 
from .models import Order,Travel,Avatar,Messages,Tours
from .forms import UserEdit,SendMessage,OrderForm
from django.views.generic import ListView
from django.views.generic.detail import DetailView
# from django.views.generic.edit import DeleteView,UpdateView,CreateView
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

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
                client = user.username,
                travel = travel.name,
                price = travel.price,
                wayToPay = data['wayToPay'],
                departure = data['departure'],
                arrival = data['arrival']
                )
            order.save()
            return render(req,'orders.html')
    else:
        order_form = OrderForm()
        return render(req,'buy.html',{'travel':travel,'order_form':order_form})
    
def contact(req):
    if req.method == 'POST':
        message_form = SendMessage(req.POST)
        if message_form.is_valid():
            data = message_form.cleaned_data
            client = req.user.username
            addressee = data['addressee']
            subject = data['subject']
            message = data['message']

            template = render_to_string('email_template.html',{
                'client' : client,
                'addressee' : addressee,
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
                client = req.user.username,
                addressee = data['addressee'],
                subject = data['subject'],
                message = data['message']
            )
            msg.save()
            return redirect('contact.html')
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
                    return render(req,'home.html',{'user':user})
                else:
                    return render(req,'login.html',{'user':f'Datos incorrectos'})
            return render(req,'login.html')
        else:
            user_form = AuthenticationForm()
            return render(req,'login.html',{"user_form":user_form})
    
def user_register(req):
    if req.method == 'POST':
        usercreate_form = UserCreationForm(req.POST)
        if usercreate_form.is_valid():
            usercreate_form.save()
            return render(req,'register.html',{"mensaje":f'usuario creado correctamente'})
        return render(req,'register.html',{"mensaje":f'error al crear el usuario, intente denuevo'})
    else:
        usercreate_form = UserCreationForm()
        return render(req,'register.html',{"usercreate_form":usercreate_form})
    
@login_required
def user_edit(req):
    user = req.user
    avatar = Avatar.objects.get(user = req.user.id)
    if req.method == 'POST':
        useredit_form = UserEdit(req.POST,instance = {'avatar':avatar,'user':user})
        if useredit_form.is_valid():
            data = useredit_form.cleaned_data
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.email = data['email']
            useredit_form.save()
            avatar = Avatar(
                user = req.user.id,
                image = data['image']
                )
            avatar.save()
            return render(req,'user.html',{"mensaje":f'usuario actualizado correctamente'})
        return render(req,'user.html',{"mensaje":f'error al actualizar el usuario, intente denuevo'})
    else:
        useredit_form = UserEdit(instance = {'avatar':avatar,'user':user})
        return render(req,'user.html',{"form":useredit_form,'avatar_img':avatar.image.url})

# @login_required
# def user_edit(req):
#     user = req.user
#     if req.method == 'POST':
#         useredit_form = UserEditForm(req.POST,instance = req.user)
#         if useredit_form.is_valid():
#             data = useredit_form.cleaned_data
#             user.first_name = data['first_name']
#             user.last_name = data['last_name']
#             user.email = data['email']
#             useredit_form.save()
#             return render(req,'user.html',{"mensaje":f'usuario actualizado correctamente'})
#         avataredit_form = AvatarEditForm(req.POST)
#         if avataredit_form.is_valid():
#             data = avataredit_form.cleaned_data
#             avatar = Avatar(
#                 user = req.user.id,
#                 image = data['image']
#                 )
#             avatar.save()
#             return render(req,'user.html',{"mensaje":f'avatar actualizado correctamente'})
#         return render(req,'user.html',{"mensaje":f'error al actualizar el avatar, intente denuevo'})
#     else:
#         avataredit_form = AvatarEditForm()
#         useredit_form = UserEditForm(instance = user)
#         return render(req,'user.html',{"useredit_form":useredit_form,"avataredit_form":avataredit_form})
# @login_required
# def user_edit(req):
#     user = req.user
#     if req.method == 'POST':
#         useredit_form = UserEditForm(req.POST,instance = req.user)
#         if useredit_form.is_valid():
#             data = useredit_form.cleaned_data
#             user.first_name = data['first_name']
#             user.last_name = data['last_name']
#             user.email = data['email']
#             useredit_form.save()
#             return render(req,'home.html',{"mensaje":f'usuario actualizado correctamente'})
#         return render(req,'user.html',{"mensaje":f'error al actualizar el usuario, intente denuevo'})
#     else:
#         useredit_form = UserEditForm(instance = user)
#         return render(req,'user.html',{"useredit_form":useredit_form})
@login_required  
def avatar_img(req):
    try:
        avatar = Avatar.objects.get(user = req.user.id)
        return render(req,'user.html',{'avatar_img':avatar.image.url})
    except:
        return render(req,'user.html')

def search(req):
    if req.GET['searchTravel']:
        search = req.GET['searchTravel']
        travel = Travel.objects.filter(name = search)
        return render(req,'search.html',{'search':travel})
    else:
        return HttpResponse(f'No se busco nada aun...')

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