from django.contrib import admin
from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('/', views.index_view, name='index'),
    path('signup/', views.signUp, name="signup"),
    path('received-messages/', views.getReceivedMessages, name='received'),
    path('sent-messages/', views.getSentMessages,name="sent"),
    path('read-messages/', views.getReadMessages, name="read"),
    path('unread-messages/', views.getUnreadMessages, name="unread"),
    path('add-message/', views.addMessage, name="add"),
    path('delete-message/<int:id>/', views.deleteMessage, name="delete"),
    path('read-a-message/<int:id>/', views.readAMessage, name="single"),
    path('unread-a-message/<int:id>/', views.unReadAMessage, name="single"),



    
    #Login
    path('signin/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signin/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
