from django.urls import path
from . import views
urlpatterns = [

    path('register/',views.RegitserView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutUserView.as_view(),name='logout'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('change_password/',views.ChangePasswordView.as_view(),name='changepassword'),
    path('send-reset-password-email/',views.SendPasswordResetEmailView.as_view(),name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/',views.UserPasswordResetView.as_view(),name='reset_password')
]
