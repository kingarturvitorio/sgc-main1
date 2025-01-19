from django.urls import path

from usuarios import views

from . import views

urlpatterns = [

    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('perfil/', views.profile, name='perfil'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('alterar_senha/', views.alterar_senha, name='alterar_senha'),
    path('logout/', views.signout, name='logout'),
]