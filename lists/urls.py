from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('/<int:id>/', views.get_delete_list, name='get_delete_list'),
    path('/<int:list_id>/items', views.get_post_item, name='get_post_item'),
    path('/<int:list_id>/items/<int:id>/', views.get_delete_update_item, name='get_delete_update_item')
]