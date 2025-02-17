
"""
URL configuration for CroquiDex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views
urlpatterns = [
    path('', views.HomeListPokemon, name='home'),
    path('equipe/', views.EquipePokemon, name='equipe'),
    path('detail/<name>', views.DetailPokemon, name='detail'),
    path('fightclub/', views.FightClubPokemon, name='fightclub'),
    path('aiduel/', views.AIDuel, name='AIDuel'),
    path('api/', views.ChatAPi, name='API'),
    path('battle/result/', views.battle_result, name='battle_result'),
]
