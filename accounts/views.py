from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'ERRO: Usuário ou senha inválidos.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Você fez login com sucesso!')

    return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('dashboard')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.error(request, 'ERRO: Nenhum campo pode estar vazio')
        return render(request, 'accounts/register.html')

    if senha != senha2:
        messages.error(request, 'ERRO: Senhas não coincidem.')
        return render(request, 'accounts/register.html')

    if len(senha) < 6:
        messages.error(request, 'ERRO: Senha mínimo de 6 caracteres.')
        return render(request, 'accounts/register.html')

    if len(usuario) < 6:
        messages.error(request, 'ERRO: Usuário mínimo de 6 caracteres.')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'ERRO: Email inválido.')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'ERRO: Usuário existente.')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'ERRO: Email existente.')
        return render(request, 'accounts/register.html')

    messages.success(request, 'Registrado com sucesso! Faça login')
    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})
    form = FormContato(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, 'ERRO: Falha ao enviar formulário')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    messages.success(request, f'Contato {request.POST.get("nome")} salvo com sucesso')
    form.save()
    return redirect('dashboard')
