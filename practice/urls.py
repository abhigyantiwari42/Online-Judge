from django.urls import path
from . import views

app_name = 'practice'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:problemid>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    #path('<int:problemid>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:problemid>/submit/', views.submit, name='submit'),
    #Leaderboard
    path('leaderboard/', views.leaderboard, name = 'leaderboard'),
    #Login
    path('login/', views.login, name = 'login'),
    #logout
    path('logout/', views.logoutUser, name = 'logout'),
    #register
    path('register/', views.register, name = 'register')
]