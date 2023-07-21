from django.urls import path

from . import views

urlpatterns = [
	path('', views.inbox, name='inbox'),
	path('<str:pk>/', views.conversation_view, name='conversation-view'),
	path('new/<str:item_pk>/', views.new_conversation, name='new'),
]
