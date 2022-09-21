from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('busca/', views.busca, name='busca'),
    path('id=<int:contato_id>', views.vercontato, name='vercontato'),

]
