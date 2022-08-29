
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .forms import ItemForm
from .models import Evento, Item  # Importação do modelo


# Create your views here.
class LoginView(TemplateView):
    """View para formulário de login de usuário"""
    template_name = 'login.html'
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('eventos')
        return render(request, self.template_name)
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('eventos')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
            return redirect('login')
    
class LogoutView(TemplateView):
    """View para logout de usuário"""

    def get(self, request):
        logout(request)
        return redirect('login')

class SignupView(TemplateView):
    """View para formulário de cadastro de usuário"""
    template_name = 'signup.html'
    user_form = UserCreationForm()
    def get(self, request):
        return render(request, self.template_name, {'form': UserCreationForm()})
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    """Mostra todos os eventos cadastrados"""
    template_name = 'index.html'

    def get(self, request):
        eventos = Evento.objects.all()
        if eventos:
            return render(request, self.template_name, {'eventos': eventos})
        else:
            return render(request, self.template_name, {'eventos': None})

@method_decorator(login_required, name='dispatch')
class ItensView(TemplateView):
    """Usuário só poderá visualizar os itens do evento se for dono do item
    ou se o item não estiver reservado"""
    template_name = 'itens.html'

    def get(self, request, id):
        itens = Item.objects.filter(Q(evento__id=id, usuario_reserva=None) | Q(evento__id=id, dono=request.user))
        evento = get_object_or_404(Evento, pk=id)
        if itens:
            return render(request, self.template_name, {'itens': itens, 'evento': evento})
        else:
            return render(request, self.template_name, {'itens': None, 'evento': evento})

@method_decorator(login_required, name='dispatch')
class ItemView(TemplateView):
    """Visualizar detalhes do item selecionado"""
    template_name = 'item.html'

    def get(self, request, id, item_id):
        item = get_object_or_404(Item, id=item_id)
        evento = get_object_or_404(Evento, id=id)
        return render(request, self.template_name, {'item': item, 'evento': evento})

@method_decorator(login_required, name='dispatch')
class ReservarItemView(TemplateView):
    """Usuário só poderá reservar um item se não for dono dele e se o item 
    não estiver reservado"""
    template_name = 'reservar.html'

    def get(self, request, id, item_id):
        item = get_object_or_404(Item, id=item_id)
        evento = get_object_or_404(Evento, id=id)
        item.usuario_reserva = request.user
        if item.usuario_reserva == item.dono:
            messages.error(request, 'Você não pode reservar seu próprio item')
            return redirect('item', id=evento.id, item_id=item.id)
        if item.usuario_reserva != None:
            messages.error(request, 'Item já reservado')
            return redirect('item', id=evento.id, item_id=item.id)
        item.save()
        return render(request, self.template_name, {'item': item, 'evento': evento})

@method_decorator(login_required, name='dispatch')
class CadastrarItemView(TemplateView):
    """Usuário pode cadastrar um item dentro do evento correspondente"""
    template_name = 'cadastrar_item.html'
    item_form = ItemForm
    
    def get(self, request, id):
        evento = get_object_or_404(Evento, id=id)
        return render(request, self.template_name, {'form': self.item_form, 'evento': evento})

    def post(self, request, id):
        evento = get_object_or_404(Evento, id=id)
        form = self.item_form(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.evento = evento
            item.dono = request.user
            item.save()
            return redirect('evento', id=evento.id)
        else:
            return render(request, self.template_name, {'form': form, 'evento': evento})
