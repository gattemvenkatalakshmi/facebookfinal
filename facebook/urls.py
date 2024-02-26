
from django.urls import path
from facebook import  views
urlpatterns = [
     path('login', views.login_page , name = 'login' ),
     path('signup',views.signup, name = 'signup'),
     path('forgot_password',views.forgot_password, name= 'forgot_password')
     
   
]
