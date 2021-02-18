from django.urls import path
from .views import loginPage, registerPage, logoutUser


app_name = 'accounts'
urlpatterns = [
    path('login/', loginPage, name='login'),
    path('register/', registerPage, name='register'),
    path('logout/', logoutUser, name='logout'),
]
