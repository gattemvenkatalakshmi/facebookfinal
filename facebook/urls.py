
from django.urls import path
from facebook import  views
urlpatterns = [
     path('login', views.login_page , name = 'login' ),
     path('signup',views.signup, name = 'signup'),
     path('forgot_password',views.forgot_password, name= 'forgot_password'),
     path('home', views.home, name ='home'),
     path('logout', views.logout,name ='logout'),
     path('friends', views.people_you_may_know, name= 'friends'),    
     path('show_Requests',views.showing_friends_request, name ='show_Requests'),
     path('view_friends',views.view_friends,name ='view_friends'),
     path('send_request/<int:id>/', views.send_request, name='send_request'),
     path('add_friend/<int:id>/', views.add_friends, name='add_friend'),
     path('reject/<int:id>/', views.remove_friends_request, name='reject'),
     # path('remove_friend/<int:friend_id>',views.remove_friend,'remove_friend'),
     path('profile', views.view_profile,name='profile'),
     path('create_post', views.create_post,name ='create_post'),
     path('my_posts',views.view_all_my_posts, name='my_posts'),
     path('like/<int:id>',views.like, name='like'),
     path('comment/<int:id>', views.save_comment, name ='comment')
    
    
     
   
]
