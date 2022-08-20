

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView

from .models import Evento  # Importação do modelo


# Create your views here.
class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return redirect('eventos')
            else:
                messages.error(request, 'Senha incorreta')
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado')
            return redirect('login')

class SignupView(TemplateView):
    template_name = 'signup.html'

    def get(self, request):
        return render(request, self.template_name, {'form': UserCreationForm()})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
        return redirect('signup')
        
class IndexView(ListView):
    template_name = 'index.html'
    model = Evento
    context_object_name = 'eventos'

    def get_queryset(self):
        return Evento.objects.all()
