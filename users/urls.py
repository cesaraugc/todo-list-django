from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_user, name='post_user'),
    path('/<int:id>/', views.get_update_user, name='get_update_user')
]