from django.urls import path
from . import views
urlpatterns = [
    path('',views.home, name='home'),
    path('room/<str:pk>',views.room, name='room'),
    path('activity/',views.activity, name='activity'),
    path('profile/<str:pk>',views.profile, name='profile'),
    path('create_room/',views.create_room, name='create_room'),
    path('update_room/<str:pk>',views.update_room, name='update_room'),
    path('delete_room/<str:pk>',views.delete_room, name='delete_room'),
    path('delete_message/<str:pk>',views.delete_message, name='delete_message'),
    path('update_user/',views.update_user, name='update_user'),
    path('topics/',views.topics, name='topics'),

    # Authentications
    path('loginuser/',views.loginuser, name='loginuser'),
    path('logoutuser/',views.logoutuser, name='logoutuser'),
    path('registeruser/',views.registeruser, name='registeruser'),
]
