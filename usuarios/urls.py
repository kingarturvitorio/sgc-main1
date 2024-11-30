from django.urls import path

from usuarios import views

app_name = "usuarios"

urlpatterns = [

    path('signin/', views.SignInView.as_view(), name='signin'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signout/', views.signout, name='signout'),
    # path('new_car/', NewCarCreateView.as_view(), name='new_car'),
]