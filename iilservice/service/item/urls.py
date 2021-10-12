from django.urls import path,include
from . import views

app_name='item'

urlpatterns = [
    path('list/', views.ItemList.as_view()),
    path('search/', views.ItemSearch.as_view()),
    path('add/', views.ItemAdd.as_view()),
    path('detail/<pk>/', views.ItemDetailView.as_view()),
    path('edit/<int:item_id>/', views.ItemEditView.as_view()),
]
