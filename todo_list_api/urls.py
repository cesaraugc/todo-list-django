from django.contrib import admin
from django.urls import include, path
from users.views import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/authenticate', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/users', include('users.urls')),
    path('api/v1/lists', include('lists.urls')),
]
