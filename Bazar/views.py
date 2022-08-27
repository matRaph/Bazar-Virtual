
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from .models import Evento  # Importação do modelo


# Create your views here.
class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('eventos')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                return redirect('eventos')
            else:
                messages.error(request, 'Credenciais inválidas')
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Credenciais inválidas')
            return redirect('login')

class LogoutView(TemplateView):
    def get(self, request):
        logout(request)
        return redirect('login')

class SignupView(TemplateView):
    template_name = 'signup.html'

    def get(self, request):
        return render(request, self.template_name, {'form': UserCreationForm()})

    def post(self, request):
        try:
            user_aux = User.objects.get(username=request.POST['username'])
            if user_aux:
                messages.error(request, 'Usuário já cadastrado')
                return redirect('signup')
        except User.DoesNotExist:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('eventos')
            else:
                messages.error(request, 'Erro ao cadastrar usuário')
                return redirect('signup')

@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request):
        eventos = Evento.objects.all()
        if eventos:
            return render(request, self.template_name, {'eventos': eventos})
        else:
            return render(request, self.template_name, {'eventos': None})

@method_decorator(login_required, name='dispatch')
class EventoView(TemplateView):
    template_name = 'evento.html'

    def get(self, request, id):
        evento = Evento.objects.get(id=id)
        return render(request, self.template_name, {'evento': evento})
