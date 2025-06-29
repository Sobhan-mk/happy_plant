from django.urls import path
from . import views

#یو آر ال های مربوط به اپ accounts در اینحا تعریف می شوند.
app_name = "accounts"
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name="login"),
    path('profile/', views.profile, name='profile'), 
    path('logout/', views.signout, name='logout'), 
    path('change_password/', views.change_password, name='change_password'),
] 
