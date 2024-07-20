from django.urls import path

from . import views
from django.contrib.sitemaps.views import sitemap
from bbguessinggame.models import *

#app_name = 'bbGuessGame'
urlpatterns = [
    path('', views.indexView, name='index'),
    path('getByName', views.getByName, name='getByName'),
    path('match', views.match, name='match'),
    ]