from django.urls import path
from . import views

# app_name = 'item'

urlpatterns = [
	path('new/', views.new_item, name='new-item'),
	path('<str:pk>/', views.detail, name='detail'),
	path('<str:pk>/delete/', views.delete, name='delete'),
]