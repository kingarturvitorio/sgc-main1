from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .forms import CreateUserForm, ProfileForm

def profile(request):
    return render(request, 'perfil.html')

def editar_perfil(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = ProfileForm(instance=request.user.profile)
    context = {'form':form}
    return render(request, 'editar_perfil.html', context)

def login_user(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f'Estou acessando o sistema')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("calendario:calendar")
        else:
            return redirect('login')
    return render(request, 'login.html')


def alterar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Atualiza a sessão para evitar logout após alteração da senha
            update_session_auth_hash(request, user)
            #messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('perfil')  # Redireciona para a página de perfil, por exemplo
        #else:
            #messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form': form}
    return render(request, 'alterar_senha.html', context)

def register_user(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('register')
        else:
            context = {'form': form}
            return render(request, 'cadastrar_usuario.html', context)

    context = {'form': form}
    return render(request, 'cadastrar_usuario.html', context)

def signout(request):
    logout(request)
    return redirect('login')
