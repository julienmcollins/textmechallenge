from django.urls import path

from . import views

app_name = 'bitly'
urlpatterns = [
    path('', views.index, name='index'),
    path('<url_id>/', views.result, name='result'),
    path('<url_id>/long/', views.long, name='long'),
]
