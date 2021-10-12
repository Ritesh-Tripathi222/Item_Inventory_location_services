from django.urls import path,include
from . import views

urlpatterns = [
    path('list/', views.LocationList.as_view()),
    path('search/', views.LocationSearch.as_view()),
    path('add/', views.LocationAdd.as_view()),
    path('detail/<pk>/', views.LocationDetail.as_view()),
    path('edit/<int:pk>/', views.LocationEdit.as_view()),
]
