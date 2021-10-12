from django.urls import path,include
from .views import InventoryAddView,InventoryListView,InventrySearch,InventoryDetailview

urlpatterns = [
    path('add', InventoryAddView.as_view(), name='add'),
    path('list', InventoryListView.as_view(), name='list'),
    path('detail/<int:pk>/', InventoryDetailview.as_view(), name='detail'),
    path('search/', InventrySearch.as_view(), name='search'),
]

