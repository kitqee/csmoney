from django.urls import path

from core import views

urlpatterns = [
    path('send-sms/', views.SMSSendCodeView.as_view(), name='send_sms'),
    path('registration/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.UserView.as_view(), name='user_detail')
]
