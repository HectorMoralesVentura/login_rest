
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from api.views import Login
from api.views import Logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/1.0/', include(('api.urls','api'))),
    path('api_generate_token/', views.obtain_auth_token),
    path('login/', Login.as_view(), name = 'login'),
    path('logout/', Logout.as_view(), name = 'Logout'),
    
]
 