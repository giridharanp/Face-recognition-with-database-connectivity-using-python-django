from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('success/', views.success, name='success'),
    path('',views.signup,name='signup'),
]
