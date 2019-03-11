from django.urls import path

from . import views

app_name = 'bitly'
urlpatterns = [
    path('', views.index, name='index'),
    path('l/', views.request_l, name='l'),
    path('s/', views.request_s, name='s'),
    path('<url_id>/', views.result, name='result'),
    path('<url_id>/long/', views.long, name='long'),
]
