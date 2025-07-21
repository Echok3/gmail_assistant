from django.urls import path
from . import views
from .views import root_redirect

urlpatterns = [
    path('', root_redirect),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('mail/<int:index>/', views.mail_detail, name='mail_detail'),  # 这一行确认在
]
